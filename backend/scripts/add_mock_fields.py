from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app('development')
with app.app_context():
    try:
        # Add mock fields to api_test_cases
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN mock_enabled BOOLEAN DEFAULT FALSE"))
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN mock_response_code INTEGER DEFAULT 200"))
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN mock_response_body TEXT"))
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN mock_response_headers JSON"))
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN mock_delay_ms INTEGER DEFAULT 0"))
        # Also add last_result
        db.session.execute(text("ALTER TABLE api_test_cases ADD COLUMN last_result JSON"))
        db.session.commit()
        print("Columns added successfully.")
    except Exception as e:
        print(f"Error adding columns (might already exist): {e}")
        db.session.rollback()
