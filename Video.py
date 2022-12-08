

class Video:
    """
        Video Class

        Stores data of a video into a class
    """
    id = ""                         # Video ID
    categories = []                 # List of Video Categories
    transcript = ""                 # Video transcript


    """
        Video Initialization Methods
        
        video_id: string
        categories: list of strings
        transcript: string
    """
    def __init__(self, video_id, categories, transcript):
        self.id = video_id
        self.categories = categories
        self.transcript = transcript

    def __int__(self, video_id, categories):
        self.id = video_id
        self.categories = categories

    def __str__(self):
        return "Video ID: " + str(self.id) +                    \
                "\n   Categories: " + str(self.categories) +    \
                "\n   Transcript: " + str(self.transcript)

    def to_dict(self):
        return {
            'video_id': self.id,
            'categories': self.categories,
            'transcript': self.transcript
        }
