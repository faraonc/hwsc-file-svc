# HWSC-File-Transaction-SVC
This is one of the microservices in the Humpback Whale Social Call project, which allows user to manage their files. 
### Purpose

This provides file management service which includes the following:
  - Downloading
  - Uploading
  - Deleting
## Prerequisites
- Python 3.7
- Webstorm

## How to install Dependencies
 - TO-DO

# How to run service
- Create a contract with API
- Develop a new service for hwsc-file-transaction-svc (e.g., Download, Upload, Delete)
- TO-DO

### 1. Upload
The path for uploading a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The uploaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The uploaded request will be sent to the file service
- The file service received connection
- The file will be sent to the file service
- The file service uploads the file to the Blob Storage
- The Blob Storage returns an url link to the file service
- The file service returns the url link to the gateway service
- The gateway service requests the metadata-file service to create a file
- The metadata-file service sends the file to MongoDB for storaging
- The MongoDB returns update to the meta-data service
- The meta-data service returns update to the gateway service.
- The file has been successfully uploaded 
### 2. Download
The path for downloading a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The downloaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The downloaded request will be sent to the file service
- The file service received connection
- TO-DO
### 3. Delete
The path for deleting a file as following:
- User logins to the gateway service
- The MongoDB checks user account and returns update to the gateway service
- The downloaded request will be sent to the metadata-file service
- The metadata-file service received connection
- The deleting request will be sent to the file service
- The file service received connection
- TO-DO