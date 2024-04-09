from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from  app.models import Internship
from  __init__ import db
app = Flask(__name__)

# Load configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://henry:victus@henry007@localhost/internconnect'
app.config['SECRET_KEY'] = 'hhh123'

# Initialize SQLAlchemy extension
db.init_app(app)


# Function to upload internship data from Excel sheet to database
def upload_internship_data(excel_file):
    with app.app_context():            
        try:
            df = pd.read_excel(excel_file)

            for index, row in df.iterrows():
                digital_id = row['Digital ID']
                organization_name = row['Name of Organisation']
                organization_address = row['Address of Organisation']
                organization_website = row['Website Link of Organisation']
                nature_of_work = row['Nature of Work']
                reporting_authority_name = row['Details of Reporting Authority']['Name']
                reporting_authority_designation = row['Details of Reporting Authority']['Designation']
                reporting_authority_email = row['Details of Reporting Authority']['Email']
                reporting_authority_mobile = row['Details of Reporting Authority']['Mobile No.']
                start_date = row['Start Date']
                completion_date = row['Completion Date']
                duration = row['Duration (months/days)']
                status = row['Status']
                mode_of_internship = row['Mode of Internship']
                stipend = True if row['Stipend'] == 'Yes' else False
                stipend_amount = row['Stipend Amount'] if stipend else None
                remarks = row['Remarks']
                offer_letter_path = row['Offer Letter']
                completion_certificate_path = row['Completion Certificate']
                internship = Internship(
                    digital_id=digital_id,
                    organization_name=organization_name,
                    organization_address=organization_address,
                    organization_website=organization_website,
                    nature_of_work=nature_of_work,
                    reporting_authority_name=reporting_authority_name,
                    reporting_authority_designation=reporting_authority_designation,
                    reporting_authority_email=reporting_authority_email,
                    reporting_authority_mobile=reporting_authority_mobile,
                    start_date=start_date,
                    completion_date=completion_date,
                    duration=duration,
                    status=status,
                    mode_of_internship=mode_of_internship,
                    stipend=stipend,
                    stipend_amount=stipend_amount,
                    remarks=remarks,
                    offer_letter_path=offer_letter_path,
                    completion_certificate_path=completion_certificate_path
                )

                # Add the internship instance to the database session
                db.session.add(internship)

                # Commit changes periodically to avoid memory overflow
                if index % 100 == 0:
                    db.session.commit()

            # Commit any remaining changes
            db.session.commit()

            return True, "Internship data uploaded successfully."
        except Exception as e:
            db.session.rollback()
            return False, f"An error occurred: {str(e)}"

if __name__ == '__main__':
    # Example usage
    excel_file_path = 'internship_data.xlsx'
    success, message = upload_internship_data(excel_file_path)
    print(message)
