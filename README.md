## 🌿 Google Image Downloader – Automated Bulk Scraper

This project is a Python-based bot that scrapes and downloads images from [Ecosia](https://www.ecosia.org/) using custom search parameters defined in a `webs.csv` file. For each search term, it creates a folder and saves a set number of high-resolution images, filtering by quality and starting index. Ideal for automated dataset creation or personal media collections.

---

### 📦 Features

* Reads multiple search terms and parameters from a CSV file.
* Automatically scrolls and loads additional images on Ecosia.
* Filters images by minimum resolution (800px, 1000px, or 1280px).
* Saves images in custom folders with sanitized filenames.
* Logs errors and warnings for failed downloads or missing images.

---

### ✅ Requirements

* Python 3.8+
* Google Chrome
* Chromedriver (manually specified path in the script)

#### Python Libraries

Install the required libraries using:

```bash
pip install beautifulsoup4 selenium requests lxml
```

---

### ⚙️ Setup

1. **Clone the repository:**

```bash
git clone https://github.com/R4INYIS/google-images-downloader/
cd google-images-downloader
```

2. **Edit the input file:**

Create or modify a `webs.csv` file with the following semicolon-separated structure:

```
Google Search;Number of Images;Image to start;Folder Name;Quality
Cats;30;0;cats_folder;2
Cars;50;5;car_images;3
```

Where:

* **Google Search**: Your search term (e.g., "Cats")
* **Number of Images**: Total images to download
* **Image to start**: Offset index
* **Folder Name**: Directory where images will be saved
* **Quality**: 1 = 800px, 2 = 1000px, 3 = 1280px minimum width

3. **Update Chromedriver path:**

Make sure the `driver_path` in `main.py` points to your local Chromedriver executable:

```python
driver_path = Service("C:\\chromedriver-win64\\chromedriver.exe")
```

---

### ▶️ How to Run

To start the scraper, simply run:

```bash
python main.py
```

The script will:

* Read each row in `webs.csv`
* Search for images on Ecosia
* Scroll to load images and filter by resolution
* Download and save images to specified folders

---

### 📝 Notes

* The script includes adaptive resolution handling: if not enough images are found, it lowers the requirement incrementally.
* A simple error log is printed at the end of execution.
* You can extend the script to support proxies, user-agent rotation, or headless mode.
