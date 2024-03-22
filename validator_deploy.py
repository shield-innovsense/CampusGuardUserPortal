

class DataValidator:
    
    def validate(self, file_name: str, class_name: str):
        return True

if __name__ == "__main__":
    validator = DataValidator()
    image_path = r"SampleVideos\WhatsApp Video 2024-03-08 at 14.52.08_d2d1a692.mp4"
    res = validator.validate(image_path, "No Helmet")
    print(res)
