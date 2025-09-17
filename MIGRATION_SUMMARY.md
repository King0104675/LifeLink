# Blood Donation System - CSV Storage Migration

## Files Modified/Created

### 1. blood_donation_app_csv.py (MAIN APPLICATION)
- **Status**: Modified from original blood_donation_app.py
- **Key Changes**:
  - Replaced in-memory dictionaries with CSV file storage
  - Added CSV handling functions: `init_csv_files()`, `read_csv_data()`, `write_csv_data()`, `add_csv_record()`
  - Added proper data type conversions for CSV storage (JSON for lists, boolean handling)
  - Created data directory structure management
  - Maintained all original Flask routes and functionality
  - Added error handling for file operations

### 2. Supporting Files Created
- **requirements.txt**: Python dependencies for the Flask application
- **README.md**: Comprehensive documentation and setup instructions
- **setup_data_files.py**: Script to initialize CSV files with proper headers
- **sample_donors.csv**: Example of donor data structure
- **sample_requests.csv**: Example of request data structure

## CSV Data Storage Structure

### Data Files (created in /data/ directory):
1. **donors.csv**: Donor registration and profile information
2. **active_requests.csv**: Blood and organ donation requests
3. **notifications.csv**: Notifications sent to compatible donors
4. **accepted_matches.csv**: Successfully matched donor-recipient pairs
5. **recipients.csv**: Recipient information (for future use)
6. **blood_banks.csv**: Blood bank information (for future use)

## Key Technical Improvements

### 1. Data Persistence
- Data now survives application restarts
- CSV files can be backed up, edited externally
- No database setup required

### 2. Data Type Handling
- Lists (like donor organs) stored as JSON strings
- Boolean values properly converted to/from strings
- Numeric values maintained with proper type conversion
- Date/timestamp handling preserved

### 3. Performance Considerations
- CSV files read/written on demand (not kept in memory)
- Efficient single-record append operations
- Proper file encoding (UTF-8) for international characters

### 4. Error Handling
- Try-catch blocks for all file operations
- Graceful handling of missing/corrupted files
- Automatic file creation with headers

## Migration Benefits

1. **No Database Required**: Eliminates need for SQL database setup
2. **Easy Backup**: Simple file copying for data backup
3. **Excel Compatibility**: Data can be viewed/edited in spreadsheet programs
4. **Version Control**: CSV files can be tracked in git
5. **Debugging**: Easy to inspect data directly in text editors
6. **Portability**: Application can be moved with just file copying

## Usage Instructions

1. Copy all HTML template files to a `templates/` folder
2. Run `python setup_data_files.py` to create initial CSV structure
3. Install dependencies: `pip install -r requirements.txt`
4. Run application: `python blood_donation_app_csv.py`
5. Access at http://localhost:5000

## Data Flow

1. **Registration**: New donors added to donors.csv
2. **Requests**: New requests added to active_requests.csv
3. **Matching**: Compatible donors found and notifications added to notifications.csv
4. **Acceptance**: Matches recorded in accepted_matches.csv
5. **Updates**: Request status updated in active_requests.csv

The system maintains full functionality while providing persistent data storage through CSV files.
