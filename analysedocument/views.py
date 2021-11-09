import json
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from analysedocument.textract import Textract
from analysedocument.analysis import TextractAnalysis

# Create your views here.
class DocumentAnalysisView(APIView):
    def get(self, request):
        document_name = request.GET.get('document_name')
        
        textract_analysis = TextractAnalysis()
        try:
            analysed_result = textract_analysis.read_analysed_document(document_name)
        except FileNotFoundError:
            analysed_result = Textract.analyse_document(document_name)
            textract_analysis.write_analysed_document(document_name, analysed_result)

        key_value_dict = textract_analysis.extract_key_value(analysed_result)
        return Response(key_value_dict, status=status.HTTP_200_OK)


class MachineLearningView(APIView):
    def post(self, request):
        request_body = json.loads(request.body)
        target_label = request_body.get('target_label')
        training_label = request_body.get('training_label')

        # Read model file
        model_file = open('trained_models/model.json', 'r')
        model_str = model_file.read()
        model_file.close()

        if model_str is None or len(model_str) == 0:
            model_str = '{}'

        # Load model data
        model = json.loads(model_str)
        trained_label_list = model.get(target_label)

        # Find training label, append if not already have
        if trained_label_list is None:
            trained_label_list = []
        
        if training_label.strip().lower() not in trained_label_list:
            trained_label_list.append(training_label.strip().lower())
            model[target_label] = trained_label_list
        
        # Update model file
        model_file = open('trained_models/model.json', 'w')
        model_file.write(json.dumps(model))

        return Response({}, status=status.HTTP_200_OK)

class PatternRecognitionView(APIView):
    def post(self, request):
        request_body = json.loads(request.body)

        # Read model file
        model_file = open('trained_models/model.json', 'r')
        model_str = model_file.read()
        model_file.close()

        if model_str is None or len(model_str) == 0:
            return Response('Model data not found', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Load model data
        model = json.loads(model_str)
        print(model)
        recognised_labels = []
        for key, value in request_body.items():
            for target_label, trained_label_list in model.items():
                if key.strip().lower() in trained_label_list:
                    recognised_labels.append({
                        'target_label': target_label,
                        'recognised_label': key,
                        'value': value
                    })

        return Response(recognised_labels, status=status.HTTP_200_OK)
