from rest_framework import viewsets,status
from rest_framework.response import Response
from .models import *
from .serializers import ClinicSerializer, DoctorSerializer, AvailableSlotSerializer, PatientSerializer
from .general_functions import *
from rest_framework.decorators import api_view
from sqlalchemy import and_
from rest_framework.views import APIView


class ClinicAPIView(APIView):
    serializer_class = ClinicSerializer

    def get(self, request, pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            clinic_id = pk
            ses = session()
            if clinic_id is None:
                clinics = ses.query(Clinic).all()
                schema = ClinicSerializer()
                result = schema.dump(clinics, many=True)
            else:
                clinics = ses.query(Clinic).filter(Clinic.id == int(clinic_id)).one()
                schema = ClinicSerializer()
                result = schema.dump(clinics)
            response_status = status.HTTP_200_OK
            response_dictionary = success_message(result)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = ClinicSerializer()
            payload = schema.load(request.data)
            ses = session()
            clinic = Clinic(name=payload['name'], address=payload['address'], contact_num=payload['contact_num'])
            ses.add(clinic)
            ses.commit()
            payload['id'] = clinic.id
            response_status = status.HTTP_201_CREATED
            response_dictionary = success_message(payload)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def put(self, request, pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = ClinicSerializer()
            payload = schema.load(request.data)
            ses = session()
            ses.query(Clinic).filter(Clinic.id == pk).update({Clinic.name: payload['name'],
                                                              Clinic.address: payload['address'],
                                                              Clinic.contact_num: payload['contact_num']},
                                                             synchronize_session=False)
            ses.commit()
            response_status = status.HTTP_200_OK
            response_dictionary = success_message('Clinic Details Updated Successfully')
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def delete(self, request, pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = ClinicSerializer()
            ses = session()
            ses.query(Clinic).filter(Clinic.id == pk).delete()
            ses.commit()
            response_status = status.HTTP_200_OK
            response_dictionary = success_message('Clinic Deleted Successfully')
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)


class DoctorAPIView(APIView):
    serializer_class = DoctorSerializer

    def get(self, request,pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            ses = session()
            doctor_id = pk
            if doctor_id is None:
                doctors = ses.query(Doctor).all()
                schema = DoctorSerializer()
                result = schema.dump(doctors, many=True)
            else:
                doctors = ses.query(Doctor).filter(Doctor.id == int(doctor_id)).one()
                schema = DoctorSerializer()
                result = schema.dump(doctors)
            response_status = status.HTTP_200_OK
            response_dictionary = success_message(result)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def post(self, request):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = DoctorSerializer()
            payload = schema.load(request.data)
            ses = session()
            clinic = ses.query(Clinic).filter(Clinic.id == payload['clinic_id']).one()
            doctor = Doctor(name=payload['name'], specialized_in=payload['specialized_in'], clinic_id=clinic.id)
            ses.add(doctor)
            ses.commit()
            payload['id'] = doctor.id
            response_status = status.HTTP_201_CREATED
            response_dictionary = success_message(payload)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def put(self, request, pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = DoctorSerializer()
            payload = schema.load(request.data)
            ses = session()
            ses.query(Doctor).filter(Doctor.id == pk).update({Doctor.name: payload['name'],
                                                              Doctor.clinic_id: payload['clinic_id'],
                                                              Doctor.specialized_in: payload['specialized_in']},
                                                             synchronize_session=False)
            ses.commit()
            response_status = status.HTTP_200_OK
            response_dictionary = success_message('Doctor Details Updated Successfully')
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)

    def delete(self, request, pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:
            schema = DoctorSerializer()
            ses = session()
            ses.query(Doctor).filter(Doctor.id == pk).delete()
            ses.commit()
            response_status = status.HTTP_200_OK
            response_dictionary = success_message('Doctor Deleted Successfully')
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)


class AppointmentAPIView(APIView):
    serializer_class = AvailableSlotSerializer

    @api_view(['GET'])
    def upcoming_available(self, request, pk=None,doctor_pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:

            ses = session()
            doc_id = int(doctor_pk)
            qry_result = ses.query(AvailableAppointmentSlot).outerjoin(ReservedAppointmentSlot). \
                filter(and_(AvailableAppointmentSlot.start_time > datetime.datetime.now(),
                            AvailableAppointmentSlot.doctor_id == 3, ReservedAppointmentSlot.id == None))
            schema = AvailableSlotSerializer()
            result_data = schema.dump(qry_result, many=True)
            response_status = status.HTTP_200_OK
            response_dictionary = success_message(result_data)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)


class PatientAPIView(APIView):
    serializer_class = PatientSerializer

    @api_view(['GET'])
    def appointments(self, request, pk=None, clinic_pk=None):
        response_status = status.HTTP_400_BAD_REQUEST
        response_dictionary = error_message("error", )
        try:

            ses = session()
            clinic_id = int(clinic_pk)
            qry_result = ses.query(Patient).join(ReservedAppointmentSlot).join(AvailableAppointmentSlot).join(Doctor). \
                filter(Doctor.clinic_id == clinic_id)
            schema = PatientSerializer()
            result_data = schema.dump(qry_result, many=True)
            response_status = status.HTTP_200_OK
            response_dictionary = success_message(result_data)
        except Exception as e:
            response_dictionary = error_message('An unknown error has occurred with message ' + str(e))

        return Response(response_dictionary, status=response_status)


