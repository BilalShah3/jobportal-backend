from rest_framework.serializers import ModelSerializer
from .models import Job, CandidatesApplied

class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields ='__all__'

class CandidatesAppliedSerializer(ModelSerializer):

    job = JobSerializer()

    class Meta:
        model = CandidatesApplied
        fields = ('user', 'resume', 'appliedAt', 'job')       


