from django.shortcuts import render

# Create your views here.

class SolicitarRegistoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        solicitacoes = SolicitarRegisto.objects.all()
        serializer = SolicitarRegistoSerializer(solicitacoes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SolicitarRegistoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolicitarRegistoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(SolicitarRegisto, pk=pk)

    def get(self, request, pk):
        solicitacao = self.get_object(pk)
        serializer = SolicitarRegistoSerializer(solicitacao)
        return Response(serializer.data)

    def put(self, request, pk):
        solicitacao = self.get_object(pk)
        serializer = SolicitarRegistoSerializer(solicitacao, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        solicitacao = self.get_object(pk)
        solicitacao.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Pagamento Views
class PagamentoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pagamentos = Pagamento.objects.all()
        serializer = PagamentoSerializer(pagamentos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PagamentoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagamentoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Pagamento, pk=pk)

    def get(self, request, pk):
        pagamento = self.get_object(pk)
        serializer = PagamentoSerializer(pagamento)
        return Response(serializer.data)

    def put(self, request, pk):
        pagamento = self.get_object(pk)
        serializer = PagamentoSerializer(pagamento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        pagamento = self.get_object(pk)
        pagamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CertificadoRegisto Views
class CertificadoRegistoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        certificados = CertificadoRegisto.objects.all()
        serializer = CertificadoRegistoSerializer(certificados, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CertificadoRegistoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificadoRegistoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(CertificadoRegisto, pk=pk)

    def get(self, request, pk):
        certificado = self.get_object(pk)
        serializer = CertificadoRegistoSerializer(certificado)
        return Response(serializer.data)

    def put(self, request, pk):
        certificado = self.get_object(pk)
        serializer = CertificadoRegistoSerializer(certificado, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        certificado = self.get_object(pk)
        certificado.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# RegistoCriminal Views
class RegistoCriminalListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        registos = RegistoCriminal.objects.all()
        serializer = RegistoCriminalSerializer(registos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistoCriminalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistoCriminalDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(RegistoCriminal, pk=pk)

    def get(self, request, pk):
        registo = self.get_object(pk)
        serializer = RegistoCriminalSerializer(registo)
        return Response(serializer.data)

    def put(self, request, pk):
        registo = self.get_object(pk)
        serializer = RegistoCriminalSerializer(registo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        registo = self.get_object(pk)
        registo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
