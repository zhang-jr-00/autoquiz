from flask import request
from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from autoquiz.extensions import db
from autoquiz.models import Document
from autoquiz.utils.pdf import extract_pdf_text, encode_file_to_base64
import os
import tempfile

# Create namespace
ns = Namespace('api/documents', description='Document operations')

# Models for Swagger documentation
document_response = ns.model('DocumentResponse', {
    'id': fields.Integer(description='Document ID'),
    'filename': fields.String(description='Original filename'),
    'upload_date': fields.String(description='Upload timestamp'),
    'content_length': fields.Integer(description='Length of extracted text'),
    'message': fields.String(description='Status message')
})

document_list_item = ns.model('DocumentListItem', {
    'id': fields.Integer(description='Document ID'),
    'filename': fields.String(description='Original filename'),
    'upload_date': fields.String(description='Upload timestamp'),
    'content_length': fields.Integer(description='Length of extracted text')
})

document_list = ns.model('DocumentList', {
    'documents': fields.List(fields.Nested(document_list_item)),
    'count': fields.Integer(description='Total number of documents')
})

error_response = ns.model('ErrorResponse', {
    'error': fields.String(description='Error message')
})

# File upload parser
upload_parser = ns.parser()
upload_parser.add_argument('file', location='files', type=FileStorage, required=True, help='PDF file')

@ns.route('')
class DocumentListResource(Resource):
    @ns.doc('list_documents')
    @ns.response(200, 'Success', document_list)
    def get(self):
        """
        Get a list of all uploaded documents
        
        This endpoint returns a list of all documents in the database.
        """
        documents = Document.query.all()
        return {
            'documents': [doc.to_dict() for doc in documents],
            'count': len(documents)
        }
    
    @ns.doc('upload_document')
    @ns.expect(upload_parser)
    @ns.response(201, 'Document uploaded successfully', document_response)
    @ns.response(400, 'Validation Error', error_response)
    @ns.response(500, 'Internal Server Error', error_response)
    def post(self):
        """
        Upload a PDF document to the database
        
        This endpoint accepts a PDF file, extracts its text content, and stores both in the database.
        """
        args = upload_parser.parse_args()
        uploaded_file = args['file']
        
        # Validate file type
        if not uploaded_file.filename.lower().endswith('.pdf'):
            return {'error': 'Only PDF files are supported'}, 400
        
        try:
            # Create a temporary file to work with pdfplumber
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                uploaded_file.save(temp.name)
                
                # Extract text from PDF
                text_content = extract_pdf_text(temp.name)
                
                # Encode file as base64
                file_base64 = encode_file_to_base64(temp.name)
            
            # Clean up temporary file
            os.unlink(temp.name)
            
            # Create new document record
            new_doc = Document(
                filename=uploaded_file.filename,
                content=text_content,
                file_data=file_base64
            )
            
            # Save to database
            db.session.add(new_doc)
            db.session.commit()
            
            response_data = new_doc.to_dict()
            response_data['message'] = 'Document uploaded successfully'
            
            return response_data, 201
            
        except Exception as e:
            return {'error': f'Error processing document: {str(e)}'}, 500

@ns.route('/<int:doc_id>')
@ns.param('doc_id', 'The document identifier')
class DocumentResource(Resource):
    @ns.doc('get_document')
    @ns.response(200, 'Success', document_response)
    @ns.response(404, 'Document not found', error_response)
    def get(self, doc_id):
        """
        Get a document by ID
        
        This endpoint retrieves a document by its ID.
        """
        document = Document.query.get(doc_id)
        
        if not document:
            return {'error': f'Document with ID {doc_id} not found'}, 404
        
        return document.to_dict()
    
    @ns.doc('delete_document')
    @ns.response(200, 'Document deleted successfully')
    @ns.response(404, 'Document not found', error_response)
    def delete(self, doc_id):
        """
        Delete a document by ID
        
        This endpoint deletes a document from the database.
        """
        document = Document.query.get(doc_id)
        
        if not document:
            return {'error': f'Document with ID {doc_id} not found'}, 404
        
        db.session.delete(document)
        db.session.commit()
        
        return {'message': f'Document with ID {doc_id} deleted successfully'}