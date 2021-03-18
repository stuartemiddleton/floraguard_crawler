class SellerInfo:

    def __init__(self, username, seller_url):
        self.username = username
        self.comments = {}
        self.profile_url = seller_url
        self.attributes = {}

    def add_item(self,url,desc):
        if url in self.comments:
            self.comments[url].append(desc)
        else:
            self.comments[url] = [desc]

    def get_profile_url(self):
        return self.profile_url

    def get_all_comments(self):
        all_comments = []
        for _, comment in self.comments.items():
            all_comments += comment

        return all_comments