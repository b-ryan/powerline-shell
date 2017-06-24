import os

def add_docker_machine_segment(powerline):
  if os.getenv('DOCKER_MACHINE_NAME'):
    powerline.append(' %s ' % os.getenv('DOCKER_MACHINE_NAME'), Color.DOCKER_MACHINE_FG, Color.DOCKER_MACHINE_BG)
