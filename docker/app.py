import tmdbsimple as tmdb
import requests
import os
from sys import platform
from alphabet_detector import AlphabetDetector
import docker
import time


tmdb.API_KEY = '678b941591dc9bdb6ec1352563253fdd'
tmdb.REQUESTS_TIMEOUT = 10
tmdb.REQUESTS_SESSION = requests.Session()

CLEAR_SYNTAXE = 'cls' if platform == 'win32' else 'clear'


tmdbMovies = tmdb.Movies()
dockerClient = docker.from_env()


def isContainerRunning(container_name):
    """
    DESC : check if container is running

    IN   : container_name - the name of the container
    OUT  : return True if it's running, else False
    """
    try:
        return dockerClient.inspect_container(container_name)['State']['Status'] == 'running'
    except Exception as e:
        print('Error func: isContainerRunning() -> {}'.format(e))
        return False

### REVIEW
def isDockerRunning(dockerComposeCommand='docker-compose up -d', restart=False):
    """
    DESC : Check if docker and Hadoop image are running

    IN   : dockerComposeCommand - command to execute to check (default: docker-compose up -d)
    OUT  : return True if it's running, else False
    """
    dockerCompose = False
    while True:
        try:
            if not(dockerCompose) or restart:
                os.system(dockerComposeCommand)
                dockerCompose, restart == True, False
            if isContainerRunning('datanode'):
                break
        except:
            print('{}\n\n\tPlease run docker before lauching program\n\n'.format(isContainerRunning('datanode')))
            quit()
        time.sleep(5)


def reqToDocker(url):
    """
    DESC : send request to the docker API

    IN   : url - endpoint
    """
    if requests.get(url) == '256': 
        print('\tZEPARTIIII')
    else:
        print('\tSomething went wrong ¯\_(ツ)_/¯')


def testDirOrCreate(name):
    """
    DESC : Test id directory exists in working directory, if not, creates it

    IN   : name - directory's name
    """
    if not os.path.isdir(name):
        try:
            os.mkdir(os.path.join('\\', os.getcwd(), name))
            print('../images directory created')
        except:
            print('Failed to create ../images directory, please launch in administrator privileges')


def movieMenu(now_playing):
    """
    DESC : Display a list of movies to choose from

    IN   : now_playing - list of recent movies
    OUT  : the position of the choosen movie
    """
    warning=''
    while True:
        os.system(CLEAR_SYNTAXE)
        print('\n\nList of available movies :\n')
        for p, movie in enumerate(now_playing):
            if AlphabetDetector().only_alphabet_chars(movie['original_title'], 'LATIN'):
                print('{} : {}'.format(p, movie['original_title']))

        choice = input('\nWhat movie do you want info on ?\n{} > '.format(warning))

        # Test if choice is an Integer in the range of the menu
        if choice.isnumeric():
            if 0 <= int(choice) <= p:
                return int(choice)
            else:
                warning='An existing one this time...\n'
        else:
            warning='A number will work great too...\n'
     


# testDirOrCreate('images')
# isDockerRunning(False)


now_playing = tmdbMovies.now_playing()['results']
movie_id=now_playing[movieMenu(now_playing)]['id']
imgPath = os.path.join(os.getcwd(), 'images', str(movie_id) + '.jpg')

if not os.path.exists(imgPath):
    with open(imgPath, 'wb') as file:
        response = requests.get(
            'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'+tmdb.Movies(movie_id).info()['poster_path'], 
            stream=True
        )
        if not response.ok:
            print('Failed to get image from Movie. Please try again ¯\_(ツ)_/¯')
        for block in response.iter_content(1024):
            if not block: break
            file.write(block)

# #  Saving image on HDFS (commands in Dockerfile, restarting container since /images binded to /hadoop/dfs/data)
# print('\n\n\tCreating HDFS directory\n')
# reqToDocker('http://localhost:5000/createHDFSDir')

# print('\n\n\tLoading to HDFS\n')
# reqToDocker('http://localhost:5000/loadToHDFS')
