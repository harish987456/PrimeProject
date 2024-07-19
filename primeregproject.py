import time
import requests
from bs4 import BeautifulSoup
import urllib3

# Suppress only the single InsecureRequestWarning from urllib3 needed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to get the project details from the detail page
def get_project_details(container):
    # Extract project details
    details = {}

    # Extract project name
    project_name_element = container.find('span', class_='font-lg fw-600')
    if project_name_element:
        details['Project Name'] = project_name_element.text.strip()

    # Extract application number
    application_number_element = container.find('a', title='View Application')
    if application_number_element:
        details['Application Number'] = application_number_element.text.strip()

    # Extract project type
    project_type_element = project_name_element.find_next('span') if project_name_element else None
    if project_type_element:
        details['Project Type'] = project_type_element.text.strip()

    # Extract contact information
    phone_element = container.select_one('.fa-mobile-alt + span')
    if phone_element:
        details['Phone'] = phone_element.text.strip()

    email_element = container.select_one('.fa-at + span')
    if email_element:
        details['Email'] = email_element.text.strip()

    # Extract address
    address_element = container.select_one('.fa-map-marker-alt + span')
    if address_element:
        details['Address'] = address_element.text.strip()

    # Extract validity date
    validity_date_element = container.select_one('.text-right .text-orange')
    if validity_date_element:
        details['Valid Upto'] = validity_date_element.text.strip()

    return details

# URL of the project detail page
url = 'https://hprera.nic.in/PublicDashboard/GetFilteredProjectsPV?DistrictList%5B0%5D.Selected=false&DistrictList%5B0%5D.Value=18&DistrictList%5B1%5D.Selected=false&DistrictList%5B1%5D.Value=24&DistrictList%5B2%5D.Selected=false&DistrictList%5B2%5D.Value=20&DistrictList%5B3%5D.Selected=false&DistrictList%5B3%5D.Value=23&DistrictList%5B4%5D.Selected=false&DistrictList%5B4%5D.Value=25&DistrictList%5B5%5D.Selected=false&DistrictList%5B5%5D.Value=22&DistrictList%5B6%5D.Selected=false&DistrictList%5B6%5D.Value=26&DistrictList%5B7%5D.Selected=false&DistrictList%5B7%5D.Value=21&DistrictList%5B8%5D.Selected=false&DistrictList%5B8%5D.Value=15&DistrictList%5B9%5D.Selected=false&DistrictList%5B9%5D.Value=17&DistrictList%5B10%5D.Selected=false&DistrictList%5B10%5D.Value=16&DistrictList%5B11%5D.Selected=false&DistrictList%5B11%5D.Value=19&PlottedTypeList%5B0%5D.Selected=false&PlottedTypeList%5B0%5D.Value=P&PlottedTypeList%5B1%5D.Selected=false&PlottedTypeList%5B1%5D.Value=F&PlottedTypeList%5B2%5D.Selected=false&PlottedTypeList%5B2%5D.Value=M&ResidentialTypeList%5B0%5D.Selected=false&ResidentialTypeList%5B0%5D.Value=R&ResidentialTypeList%5B1%5D.Selected=false&ResidentialTypeList%5B1%5D.Value=C&ResidentialTypeList%5B2%5D.Selected=false&ResidentialTypeList%5B2%5D.Value=M&AreaFrom=&AreaUpto=&SearchText='  # Replace with your actual URL

# Make a GET request to the URL and ignore SSL certificate verification (not recommended for production)
response = requests.get(url, verify=False)

# Check if the request was successful
if response.status_code == 200:
    time.sleep(10)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all project detail containers
    project_containers = soup.find_all('div', class_='col-lg-6')

    # Print number of project containers found
    print(f"Found {len(project_containers)} project containers")

    # List to store all projects details
    projects = []

    # Iterate over each project container and extract details
    for container in project_containers:
        project_details = get_project_details(container)
        if project_details:
            projects.append(project_details)

    # Print the extracted details
    if projects:
        print("Extracted Project Details:")
        for i, project in enumerate(projects, 1):
            print(f"Project {i}:")
            for key, value in project.items():
                print(f"  {key}: {value}")
            print()
    else:
        print("No project details found.")
else:
    print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")