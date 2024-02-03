# Amenity-Detection-using-Detectron2
**Purpose:** <br>
Short-term rentals facilitated by platforms like Airbnb have gained immense popularity, providing property owners with a lucrative venture. However, concerns about property conditions after check-out persist. This research addresses this challenge by developing **deep learning and computer vision** tools for amenity detection and inventory tracking. Specifically, the goal is to assist hosts in managing property details efficiently, improving transparency, and enhancing the overall rental experience.

**Tasks:** <br>
The research employs the **CRISP-DM** methodology in six essential stages. Initial steps involve information gathering on object detection and inventory management, leading to the creation of a taxonomy of 32 image classes. Data collection utilizes open-source datasets like Open Images V7 and Google Simple Images. Data preparation involves annotation using tools like Labelme and Roboflow, addressing imbalances in class distribution. The dataset is then fed into state-of-the-art object detection models like **Detectron2-Mask R-CNN, YOLOv7, EfficientDet, RetinaNet, and DETR**. The best model is selected based on performance metrics and deployed in a web application.

**Outcomes:** <br>
The team successfully develops 'Amenitrack,' a web application predicting property amenities based on images uploaded by hosts or guests. The deep learning models trained and finetuned on our custome dataset facilitate automated amenity detection, enhancing property management. The application provides a platform for hosts to analyze and monitor amenities through **charts and maps**, improving transparency for guests and hosts alike. Results indicate that the **YOLO V7** model outperformed others with an **mAP score of 0.86**, showcasing its efficacy in amenity detection.

**Tech Stack Used:** <br>
Data Collection , Preprocessing, Preparation: Google api, OpenImages v7, Roboflow, Python, LabelME
Data modelling and database management: MySQl, Google cloud sql
Model training: Google colab Pro, Pytorch, tensorflow
Data Visualization: Matplotlib, Seaborn, Tableau, Folium api
object detection: YOLO V7, EfficientDet, RetinaNet, Detection Transformers
Image segmentation: Detectron2 Mask RCNN

**Applications:** <br>
Beyond its application in short-term rentals, Amenitrack has potential uses in inventory management across various domains such as warehouses, workshops, exhibition halls, and schools. The tool's versatility makes it adaptable to different environments, impacting productivity and efficiency.

**Conclusion:** <br>
The project follows the CRISP-DM methodology, emphasizing data quality and model evaluation. While successful in achieving its objectives, the application has limitations related to image quality and predefined amenity types. The benefits include automated amenity detection, real-time inventory updates, improved guest experiences, and a competitive advantage.

**Recommendations for Future Work:** <br>
Future work involves improving accuracy through dataset expansion, adding new amenity types, integrating with Airbnb, implementing color detection, developing a mobile application, and incorporating localization features. These enhancements aim to address current limitations and broaden the tool's scope.

**Contributions and Impacts on Society:** <br>
The project's impact extends beyond property management, potentially transforming inventory management across sectors, enhancing efficiency, safety, and operational processes in various industries


# Authors: Nilisha Makam Prashantha, Joshnadevi Vadapalli, Sangamithra Murugesan, Faiza Ayoun




