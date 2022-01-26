from pywebhdfs.webhdfs import PyWebHdfsClient
import requests
import docker
import time
import os


class DockerManager(object):
    def __init__(self, api_url='http://localhost:9870', host='localhost', port='9870'):
        """
        DESC : create a docker client from the dockerfile locate on the same directory level

        IN   : api_url - base url for docker small custom flask api 
        """
        self.docker_client = docker.from_env()
        self.api_docker_base_url = api_url
        self.hdfs = PyWebHdfsClient(host=host,port=port, user_name=None)

    def isContainerRunning(self, container_name):
        """
        DESC : check if container is running

        IN   : container_name - the name of the container
        OUT  : return True if it's running, else False
        """
        try:
            return self.docker_client.inspect_container(container_name)['State']['Status'] == 'running'
        except Exception as e:
            print('Error :' + e)
            return False

    def isDockerRunning(self, dockerComposeCommand='docker-compose up -d', restart=False):
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
                if self.isContainerRunning('datanode'):
                    break
            except:
                print('\n\n\tPlease run docker before lauching program\n\n')
                quit()
            time.sleep(5)


    def createHDFSDirectory(self):
        """
        DESC : send request to create directory in HDFS
        """
        try :
            self.hdfs.make_dir('/FilmPosters')
            print('HDFS directory created !')
        except requests.exceptions.ConnectionError :
            print('Impossible to create HDFS Directory')


    def deleteHDFSDirectory(self):
        """
        DESC : send request to delete directory in HDFS
        """
        try :
            requests.delete("http://localhost:9870/webhdfs/v1/FilmPosters?op=DELETE&recursive=true")
            print('HDFS directory deleted !')
        except requests.exceptions.ConnectionError :
            print('Deletion of HDFS directory failed.')


    def reqToDocker(self, endpoint):
        """
        DESC : send request to the docker API

        IN   : url - endpoint
        """
        if requests.get(self.api_docker_base_url + endpoint) == '256': 
            print('\tZEPARTIIII')
        else:
            print('\tSomething went wrong ¯\_(ツ)_/¯')



