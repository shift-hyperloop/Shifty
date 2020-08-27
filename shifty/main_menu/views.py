from django.shortcuts import render

class HomeView:
    """
    Class for the home view
    """

    @staticmethod
    def home(request):
        """
        Function for displaying home page
        :param request: The http request
        :return: The rendered HTML file
        """
        
        return render(request, 'main_menu/home.html')

