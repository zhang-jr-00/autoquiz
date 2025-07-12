from autoquiz.extensions import db
import datetime

class Document(db.Model):
    """
    Model for storing uploaded PDF documents.
    - id: Primary key
    - filename: Original filename 
    - content: Extracted text content from the PDF
    - file_data: Base64 encoded PDF file data
    - upload_date: When the document was uploaded
    """
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=True)
    file_data = db.Column(db.Text, nullable=False)  # Base64 encoded file
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<Document {self.filename}>'
    
    def to_dict(self):
        """Convert the model to a dictionary for API responses"""
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat(),
            'content_length': len(self.content) if self.content else 0
        }