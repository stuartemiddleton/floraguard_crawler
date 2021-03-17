class UserInfo:

    def __init__(self, username, profile_url):
        self.username = username
        self.comments = {}
        self.attributes = {}
        self.profile_url = profile_url

    def add_comment(self, comment, thread,url):
        if url in self.comments:
            # Limiting it to the most recent 100 comments in order to keep the memory impact low
            if len(self.comments) > 100:
                self.comments[url].pop()
            self.comments[url].append(comment)
        else:
            self.comments[url] = [comment]

    def add_attribute(self, attribute_name, attribute):
        if attribute_name in self.attributes:
            self.attributes[attribute_name] += [attribute]
        else:
            self.attributes[attribute_name] = [attribute]

    def get_profile_url(self):
        return self.profile_url

    def get_all_comments(self):
        all_comments = []
        for thread, comments in self.comments.items():
            all_comments += comments

        return all_comments

    def __str__(self):
        return "Username: " + self.username + "\nProfile URL extention: " + self.profile_url + "\nAttributes: " + str(
            self.attributes) + "\nList of comments:" + str(self.comments)
