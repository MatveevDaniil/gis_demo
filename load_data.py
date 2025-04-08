import os
import wget
import zipfile
import kagglehub


def load_odcm():
  # https://www.kaggle.com/datasets/vinven7/comprehensive-database-of-minerals
  path = kagglehub.dataset_download("simonjasansky/open-database-on-global-coal-and-metal-mining")
  print("Path to dataset files:", path)


def load_africa():
  # u can also load it manually from https://data.usgs.gov/datacatalog/data/USGS:607611a9d34e018b3201cbbf
  base_url = "https://www.sciencebase.gov/catalog/file/get/607611a9d34e018b3201cbbf"
  files = {
    "Africa_GIS_Metadata.xml": "f=__disk__97%2Fa8%2F1c%2F97a81ce9e362ed344226f8ca36776ec58c10ff45",
    # "Africa_GIS.gdb.zip": "f=__disk__30%2F8a%2Fb1%2F308ab140de2e0a1384172068209374d19ae4a65a", # needed only for arcgis
    "Africa_GIS_Supporting_Data.zip": "f=__disk__34%2F4b%2Fcb%2F344bcb00f8be64dc390047b679eb0bec50dd95d5"
  }

  output_folder = "downloads"
  os.makedirs(output_folder, exist_ok=True)

  for filename, path in files.items():
    url = f"{base_url}?{path}"
    output_path = os.path.join(output_folder, filename)
    wget.download(url, out=output_path)
    if filename.endswith(".zip"):
      extract_dir = os.path.join(output_folder, filename.replace(".zip", ""))
      os.makedirs(extract_dir, exist_ok=True)
      with zipfile.ZipFile(output_path, 'r') as z:
        z.extractall(extract_dir)

def unzip_and_clean(folder_path):
    for root, dirs, files in os.walk(folder_path):
      for file in files:
        if file.endswith('.zip'):
          zip_path = os.path.join(root, file)
          extract_dir = os.path.join(root, file.replace('.zip', ''))
          os.makedirs(extract_dir, exist_ok=True)
          with zipfile.ZipFile(zip_path, 'r') as z:
              z.extractall(extract_dir)
          os.remove(zip_path)

if __name__ == '__main__':
  # load_odcm()
  load_africa()
  unzip_and_clean('downloads/Africa_GIS_Supporting_Data')
  # unzip_and_clean('downloads/Africa_GIS.gdb')