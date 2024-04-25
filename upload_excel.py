import pandas as pd
from  app.models import Internship
from app import create_app
from app.extensions import db
from dotenv import load_dotenv

load_dotenv()
app=create_app()

# Function to upload internship data from Excel sheet to database
def upload_internship_data(excel_file):
    with app.app_context():            
        try:
            df = pd.read_excel(excel_file)
            stipend_amount = None

            for index, row in df.iterrows():
                digital_id = row['digital_id']
                org_name = row['org_name']
                org_address = row['org_address']
                org_website = row.get('org_website', None)
                nature_of_work = row['nature_of_work']
                reporting_authority = row['reporting_authority']
                start_date = row['start_date']
                completion_date = row['end_date']
                duration = row['Duration (Months / Days)']
                ppo = "Yes" if row['ppo'] == 'PPO Received' else None
                status = row['internship_status']
                mode_of_internship = row['internship_mode']
                stipend = True if row['stipend'] == 'Yes' else False
            if stipend:
                stipend_amount_value = row['stipend_amount']
                if isinstance(stipend_amount_value, str):
                    digit_chars = ''.join(char for char in stipend_amount_value if char.isdigit())
                    
                    if digit_chars:
                        stipend_amount = int(digit_chars)
                    else:
                        stipend_amount = None
                elif isinstance(stipend_amount_value, (float, int)):
                    stipend_amount = int(stipend_amount_value)
                else:
                    stipend_amount = None

                # remarks = row.get('Remarks', None)
                offer_letter_path = row['offer_letter']
                completion_letter_path = row['completion_letter']
                internship = Internship(
                    digital_id=digital_id,
                    org_name=org_name,
                    org_address=org_address,
                    org_website=org_website,
                    nature_of_work=nature_of_work,
                    reporting_authority=reporting_authority,
                    start_date=start_date,
                    end_date=completion_date,
                    # duration=duration,
                    internship_status=status,
                    internship_mode=mode_of_internship,
                    ppo=ppo,
                    stipend=stipend,
                    stipend_amount=stipend_amount,
                    # remarks=remarks,
                    offer_letter=offer_letter_path,
                    completion_letter=completion_letter_path
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
