import pandas as pd
from app.models import Internship
from app import create_app
from app.extensions import db
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Create the app
app = create_app()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to upload internship data from Excel sheet to database
def upload_internship_data(excel_file):
    with app.app_context():
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(excel_file)
            
            # Process each row in the DataFrame
            for index, row in df.iterrows():
                # Extract data from the row and replace NaN values with None
                digital_id = row.get('digital_id')
                org_name = row.get('org_name')
                org_address = row.get('org_address', None)
                org_website = row.get('org_website', None)
                nature_of_work = row.get('nature_of_work', None)
                reporting_authority = row.get('reporting_authority', None)
                start_date = row.get('start_date')
                end_date = row.get('end_date')
                internship_status = row.get('internship_status')
                internship_mode = row.get('internship_mode')
                ppo = "Yes" if row.get('ppo') == 'PPO Received' else None
                stipend = row.get('stipend') == 'Yes'

                # Handle stipend_amount
                stipend_amount = None
                if stipend:
                    stipend_amount_value = row.get('stipend_amount')
                    # Handle different types of stipend_amount_value
                    if pd.isna(stipend_amount_value):
                        stipend_amount = None
                    elif isinstance(stipend_amount_value, (float, int)):
                        stipend_amount = int(stipend_amount_value)
                    elif isinstance(stipend_amount_value, str):
                        # Extract digit characters and convert to integer
                        digit_chars = ''.join(char for char in stipend_amount_value if char.isdigit())
                        if digit_chars:
                            stipend_amount = int(digit_chars)
                        else:
                            stipend_amount = None

                # Replace NaN values with None for relevant fields
                offer_letter = row.get('offer_letter')
                completion_letter = row.get('completion_letter')

                if pd.isna(offer_letter):
                    offer_letter = None
                if pd.isna(completion_letter):
                    completion_letter = None

                # Create an Internship object
                internship = Internship(
                    digital_id=digital_id,
                    org_name=org_name,
                    org_address=org_address,
                    org_website=org_website,
                    nature_of_work=nature_of_work,
                    reporting_authority=reporting_authority,
                    start_date=start_date,
                    end_date=end_date,
                    internship_status=internship_status,
                    internship_mode=internship_mode,
                    ppo=ppo,
                    stipend=stipend,
                    stipend_amount=stipend_amount,
                    offer_letter=offer_letter,
                    completion_letter=completion_letter
                )

                # Add the internship instance to the database session
                db.session.add(internship)

                # Commit changes periodically to avoid memory overflow
                if index % 100 == 0:
                    db.session.commit()

            # Commit any remaining changes
            db.session.commit()

            logger.info("Internship data uploaded successfully.")
            return True, "Internship data uploaded successfully."
        except Exception as e:
            # Rollback the transaction in case of an error
            db.session.rollback()
            
            # Log the error for debugging
            logger.error(f"An error occurred: {str(e)}")
            
            return False, f"An error occurred: {str(e)}"

if __name__ == '__main__':
    # Example usage
    excel_file_path = 'internship_data.xlsx'
    success, message = upload_internship_data(excel_file_path)
    print(message)
