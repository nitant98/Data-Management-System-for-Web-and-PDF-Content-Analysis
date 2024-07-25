import csv
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
from Validation import URLClass 


def webscrape():
    session = HTMLSession()

    base_url_pattern = 'https://www.cfainstitute.org/en/membership/professional-development/refresher-readings'

    # Parameters for URL generation
    sort_order = '%40refreadingcurriculumyear%20descending'
    number_of_results_per_page = 100
    total_number_of_pages = 3  # Update this if there are more pages

    # Generate URLs dynamically
    base_urls = [
        f"{base_url_pattern}#sort={sort_order}&first={page * number_of_results_per_page}&numberOfResults={number_of_results_per_page}"
        for page in range(total_number_of_pages)
    ]

    # CSV file setup
    csv_file_path = 'CSV/extracted_updated.csv'
    headers = ['Name_of_the_topic', 'Year', 'Level', 'Introduction_Summary', 'Learning_Outcomes', 'Link_to_the_Summary_Page', 'Link_to_the_PDF_File']

    def safe_extract_text(soup, selector, attribute=None):
        element = soup.select_one(selector)
        if attribute and element:
            return element[attribute] if attribute in element.attrs else None
        return element.get_text(strip=True) if element else None

    def extract_following_text(header):
        if header:
            content = []
            for sibling in header.find_next_siblings():
                if sibling.name == "h2":
                    break  # Stop if we encounter another header
                content.append(sibling.get_text(strip=True))
            return " ".join(content)
        return None

    def scrape_links(html):
        links = []
        for link in html.find('div.coveo-result-cell a.CoveoResultLink'):
            href = link.attrs['href']
            if href:
                links.append(href)
        return links

    def safe_extract_pdf_link(soup, selector):
        links = soup.select(selector)
        for link in links:
            href = link.get('href', '')
            if href.endswith('.pdf'):
                if href.startswith('/-/media'):
                    return f"https://www.cfainstitute.org{href}"
                return href
        return "N/A"

    def extract_year_from_string(input_string): 
        match = re.search(r'\d{4}', input_string)
        if match:
            return int(match.group(0))  # Convert the matched string to integer
        else:
            return None

    # Scrape all links from each base URL
    all_links = []
    for base_url in base_urls:
        response = session.get(base_url)
        response.html.render(wait=20, sleep=5)
        all_links.extend(scrape_links(response.html))

    # Now process each link and write details to the CSV
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for link in all_links:
            # Fetch the detailed page
            detailed_response = requests.get(link)
            detailed_soup = BeautifulSoup(detailed_response.content, 'html.parser')
            
            # Extract the required information
            topic = safe_extract_text(detailed_soup, ".content-utility-topics")
            year = safe_extract_text(detailed_soup, ".content-utility-curriculum")

            # Fill Null values in Topic
            if topic is None:
                topic = 'Not Available'

            # Extract Year from String
            if year is None:
                year = 9999
            else:
                year = extract_year_from_string(year)
            
            level = safe_extract_text(detailed_soup, ".content-utility-level")
            
            # Use the new function to extract PDF links
            pdf_link = safe_extract_pdf_link(detailed_soup, "a[href]")

            # Making sure links start with htttp
            if pdf_link and not pdf_link.startswith("http"):
                pdf_link = f"https://www.cfainstitute.org{pdf_link}"
            
            introduction_header = detailed_soup.find("h2", string="Introduction")
            introduction_text = extract_following_text(introduction_header)
            
            learning_outcomes_header = detailed_soup.find("h2", string="Learning Outcomes")
            learning_outcomes_text = extract_following_text(learning_outcomes_header)
            
            data = {
                'Name_of_the_topic': topic or "N/A",
                'Year': year or "N/A",
                'Level': level or "N/A",
                'Introduction_Summary': introduction_text or "N/A",
                'Learning_Outcomes': learning_outcomes_text or "N/A",
                'Link_to_the_Summary_Page': link,
                'Link_to_the_PDF_File': pdf_link  # Use the extracted PDF link
            }
            
            writer.writerow(data)

def clean_validate_csv():
    csv_file_path = 'CSV/extracted_updated.csv'
    url_class_instance = URLClass(str(csv_file_path))
    valid_topics, validation_errors = url_class_instance.clean_and_validate_csv()
    print(f"Valid rows: {len(valid_topics)}, Validation errors: {len(validation_errors)}")
    if validation_errors:
        print("Validation Errors Encountered:")
        for error in validation_errors:
            print(f"Row: {error['row']}")
            print(f"Error: {error['error']}\n")
    else:
        print("No validation errors encountered.")

if __name__ == "__main__":
    webscrape()
    clean_validate_csv()