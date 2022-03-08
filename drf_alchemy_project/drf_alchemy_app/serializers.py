from marshmallow import Schema, fields


class ClinicSerializer(Schema):
    id = fields.Integer()
    name = fields.Str()
    address = fields.Str()
    contact_num = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()


class DoctorSerializer(Schema):
    id = fields.Integer()
    name = fields.Str()
    specialized_in = fields.Str()
    clinic_id = fields.Integer()
    clinic = fields.Nested('ClinicSerializer', exclude=("created_at", "updated_at", "is_deleted",))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()


class PatientSerializer(Schema):
    name = fields.Str()


class AvailableSlotSerializer(Schema):
    id = fields.Integer()
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    doctor_id = fields.Integer()
    # doctor = fields.Nested('DoctorSerializer', exclude=("created_at", "updated_at", "is_deleted",))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()


class ReservedSlotSerializer(Schema):
    id = fields.Integer()
    status = fields.Str()
    available_slot_id = fields.Integer()
    available_slot = fields.Nested('AvailableSlotSerializer', exclude=("created_at", "updated_at", "is_deleted",))
    patient_id = fields.Integer()
    # patient = fields.Nested('PatientSerializer', exclude=("created_at", "updated_at", "is_deleted",))
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    is_deleted = fields.Boolean()
