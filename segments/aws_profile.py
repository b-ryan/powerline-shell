
def add_aws_profile_segment(powerline):
    import os

    aws_profile = os.environ.get('AWS_PROFILE') or \
        os.environ.get('AWS_DEFAULT_PROFILE')

    if aws_profile:
        powerline.append(' aws:%s ' % os.path.basename(aws_profile),
                         Color.AWS_PROFILE_FG,
                         Color.AWS_PROFILE_BG)
