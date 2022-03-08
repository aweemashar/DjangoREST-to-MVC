from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa
import datetime

# engine = db.create_engine('mysql+mysqldb://root:AAB123lahore@localhost:3306/appointment_management_system')

engine = sa.create_engine('mysql+mysqldb://root:AAB123lahore@localhost:3306/Appointment_Management', echo=True)
session = sa.orm.scoped_session(sa.orm.sessionmaker(bind=engine))

Base = declarative_base()
Base.query = session.query_property()


class Clinic(Base):
    __tablename__ = 'clinic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    address = Column(String)
    contact_num = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


class Doctor(Base):
    __tablename__ = 'doctor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    clinic_id = Column(Integer, ForeignKey('clinic.id'))
    clinic = relationship(Clinic, backref=backref('doctor', uselist=True))
    name = Column(String)
    specialized_in = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


class Patient(Base):
    __tablename__ = 'patient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_num = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


class AvailableAppointmentSlot(Base):
    __tablename__ = 'available_appointment_slot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey('doctor.id'))
    doctor = relationship(Doctor, backref=backref('available_slot', uselist=True))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


class ReservedAppointmentSlot(Base):
    __tablename__ = 'reserved_appointment_slot'
    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('available_appointment_slot.id'))
    appointment = relationship(AvailableAppointmentSlot, backref=backref('reserve_slot_appointment', uselist=True))
    patient_id = Column(Integer, ForeignKey('patient.id'))
    patient = relationship(Patient, backref=backref('reserve_slot_patient', uselist=True))
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_deleted = Column(Boolean, default=False)


Base.metadata.create_all(engine)


