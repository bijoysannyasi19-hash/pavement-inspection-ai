"""
Dataset Preparation Script for Pavement Asset Management System
Handles downloading, unzipping, and converting RDD2022 XML (Pascal VOC) to YOLO format.
"""
import os
import glob
import xml.etree.ElementTree as ET
from pathlib import Path
from sklearn.model_selection import train_test_split
import yaml
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatasetPreprocessor:
    def __init__(self, data_dir: str, config_path: str):
        self.data_dir = Path(data_dir)
        self.config_path = Path(config_path)
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
            
        # Reverse map to convert string labels to integer ids
        self.class_mapping = {v: k for k, v in self.config['classes'].items()}

    def convert_voc_to_yolo(self, size: tuple, box: tuple) -> tuple:
        """
        Convert Pascal VOC bounding box (xmin, ymin, xmax, ymax) 
        to YOLO format (x_center, y_center, width, height) normalized to 0-1.
        """
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (box[0] + box[1]) / 2.0
        y = (box[2] + box[3]) / 2.0
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)

    def process_xml_annotations(self, xml_dir: Path, img_dir: Path, output_dir: Path):
        """
        Process directory of XML files and generate YOLO format txt files.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        xml_files = glob.glob(os.path.join(xml_dir, "*.xml"))
        
        logging.info(f"Processing {len(xml_files)} XML annotations...")
        for xml_file in xml_files:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            size = root.find('size')
            w = int(size.find('width').text)
            h = int(size.find('height').text)
            
            img_id = Path(xml_file).stem
            txt_file_path = output_dir / f"{img_id}.txt"
            
            with open(txt_file_path, 'w') as out_file:
                for obj in root.iter('object'):
                    difficult = obj.find('difficult').text if obj.find('difficult') is not None else 0
                    cls_name = obj.find('name').text
                    
                    if cls_name not in self.class_mapping or int(difficult) == 1:
                        continue
                        
                    cls_id = self.class_mapping[cls_name]
                    xmlbox = obj.find('bndbox')
                    b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), 
                         float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                    bb = self.convert_voc_to_yolo((w, h), b)
                    out_file.write(f"{cls_id} " + " ".join([str(a) for a in bb]) + '\n')
                    
    def split_dataset(self, img_dir: Path, label_dir: Path, test_size: float = 0.2, val_size: float = 0.1):
        """
        Split dataset into train, val, and test sets and organize files.
        """
        logging.info("Splitting dataset into train, val, test...")
        all_imgs = glob.glob(os.path.join(img_dir, "*.jpg"))
        
        train_imgs, test_imgs = train_test_split(all_imgs, test_size=test_size, random_state=42)
        
        # Calculate relative validation size
        val_relative = val_size / (1 - test_size)
        train_imgs, val_imgs = train_test_split(train_imgs, test_size=val_relative, random_state=42)
        
        splits = {'train': train_imgs, 'val': val_imgs, 'test': test_imgs}
        
        for split, imgs in splits.items():
            split_img_dir = self.data_dir / 'images' / split
            split_label_dir = self.data_dir / 'labels' / split
            split_img_dir.mkdir(parents=True, exist_ok=True)
            split_label_dir.mkdir(parents=True, exist_ok=True)
            
            for img_path in imgs:
                img_name = Path(img_path).name
                label_name = img_name.replace('.jpg', '.txt')
                
                # Copy image
                shutil.copy(img_path, split_img_dir / img_name)
                
                # Copy label if exists
                label_src = label_dir / label_name
                if label_src.exists():
                    shutil.copy(label_src, split_label_dir / label_name)
                    
        logging.info("Dataset splitting completed.")
        
    def generate_yolo_yaml(self):
        """
        Generate dataset.yaml for YOLO training.
        """
        yaml_content = {
            'path': str(self.data_dir.absolute()),
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'names': self.config['classes']
        }
        
        with open(self.data_dir / 'dataset.yaml', 'w') as f:
            yaml.dump(yaml_content, f, sort_keys=False)
        logging.info(f"Generated dataset.yaml at {self.data_dir / 'dataset.yaml'}")

if __name__ == "__main__":
    # Example Usage (assuming raw data is placed in data/raw)
    # preprocessor = DatasetPreprocessor("data", "config/parameters.yaml")
    # preprocessor.process_xml_annotations(Path("data/raw/annotations"), Path("data/raw/images"), Path("data/raw/labels"))
    # preprocessor.split_dataset(Path("data/raw/images"), Path("data/raw/labels"))
    # preprocessor.generate_yolo_yaml()
    pass
