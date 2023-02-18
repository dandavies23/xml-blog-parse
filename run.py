import csv
import xml.etree.ElementTree as ET

# Change file path for XML export file
tree = ET.parse('xml-backups/track23.wordpress.2020-01-27.xml')
root = tree.getroot()

# Open a new CSV file for writing -- change title to test different backups
with open('blog-posts.csv', mode='w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Title', 'Publication Date', 'Author', 'Body', 'Tags', 'Featured Image'])

    # Loop through each post in the XML file
    for item in root.findall('./channel/item'):

        # Check if the post is a blog post
        post_type = item.find('wp:post_type', {'wp': 'http://wordpress.org/export/1.2/'}).text
        if post_type == 'post':

            # Extract the relevant fields from the post
            title = item.find('title').text
            pub_date = item.find('pubDate').text
            author = item.find('dc:creator', {'dc': 'http://purl.org/dc/elements/1.1/'}).text
            body = item.find('content:encoded', {'content': 'http://purl.org/rss/1.0/modules/content/'}).text
            tags = [tag.text for tag in item.findall('category')]
                       
            # Check if the post has a featured image and extract the URL
            if item.find('wp:attachment_url', {'wp': 'http://wordpress.org/export/1.2/'}):
                featured_image = item.find('wp:attachment_url', {'wp': 'http://wordpress.org/export/1.2/'}).text
            else:
                featured_image = ""

            # Write the data to a new row in the CSV file
            writer.writerow([title, pub_date, author, body, ', '.join(tags), featured_image])
