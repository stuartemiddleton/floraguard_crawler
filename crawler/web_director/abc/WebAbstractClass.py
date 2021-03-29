from abc import ABC, abstractmethod

"""
    Abstract class which each new website inherits, by providing the basic functions in this
    class, any implemtation of this class can be used for the directed crawler. Filling out 
    this class is a simple task.
    
"""


class WebpageAbstractClass(ABC):
    """
        Link containing the root page
        return: The string of the link 
    """

    @abstractmethod
    def get_root_page_url(self):
        pass

    """
        Link containing the threads hub page
        return: The string of the link 
    """

    @abstractmethod
    def get_general_start_page_url(self):
        pass

    """
        Link containing the general thread page
        return: The string of the link 
    """

    @abstractmethod
    def get_general_page_url(self):
        pass

    """
        Link containing the general profile page
        return: The string of the link
    """

    @abstractmethod
    def get_general_profile_url(self):
        pass

    """
        Regex to return the name of the thread
        
    """

    @abstractmethod
    def thread_name_regex(self):
        pass

    """ 
        BLOCK REGEX 
        The block regex is the regex containing the entire block of post on a thread
        This includes the comment, profile and link to profile. The regex following this
        is how to get those following fields from the block 
        return: The regex for beautiful soup to get the block
    """

    @abstractmethod
    def block_regex(self):
        pass

    """
        The regex to get the comment from the block
        return: The regex for beautiful soup to get the comment
    """

    @abstractmethod
    def comment_regex(self):
        pass

    """
        The regex to get the profile from the block
        return: The regex for beautiful soup to get the profile
    """

    @abstractmethod
    def profile_regex(self):
        pass

    """
        The regex to get the profile name from the block
        return: The regex for beautiful soup to get the profile name (Note that this is following the profile regex)
    """

    @abstractmethod
    def profile_name_regex(self):
        pass

    """
        The regex to get the profile link from the block
        return: The regex for beautiful soup to get the profile name (Note that this is following the profile regex)
    """

    @abstractmethod
    def profile_link_regex(self):
        pass

    """ 
        PROFILE REGEX
        On the profile page there is a collection of attributes that can be collected from the page, this
        function returns a dictionary of regex patters to grab the attributes. The key value pair shows the 
        name of the attribute with the regex to get that attribute
        return: The dictionary of attribute name to regex to get it
    """

    @abstractmethod
    def attributes_regex(self):
        pass


    @abstractmethod
    def date_regex(self):
        pass
