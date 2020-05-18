from flask import Blueprint
from flask_restx import Api, Model, fields

# blueprint = Blueprint('api', __name__)
# api = Api(blueprint)

"""--------------- API request and response models ------------------"""

#generic response model
response_model = Model("Response", {
    "status": fields.String(description="Status", required=True, enum=["success", "error"]),
    "message": fields.String(description="Message from server", required=True),
})

# user created response model
user_response = Model("Response", {
    "action": fields.String(description="Update action", require=True, enum=["created", "verified", "updated", "deleted"]),
    "user": {
        "username": fields.String(description="Username", required=True)
    }
})


#this should be person name
person_model = Model("Persoon", {
        "id": fields.String(description="IDRegent"),
        "fullname": fields.String(description="fullname"),
        "normalized_fullname": fields.String(description="normalized_fullname"),
        "aanstellingen": fields.List((fields.String)),
        "references": fields.List((fields.String)),
        #"by": fields.String(description="birth year"),
        #"dy": fields.String(description="death year"),
        #"bio": fields.String(description="biography notes"),
        #"birth":fields.String(description="birth day (full)"),
        #"death":fields.String(description="death day (full)"),
        #"reference":fields.String(description="reference to other name")
        })

person_response = response_model.clone("Persoon",
                            {"personname": fields.Nested(person_model)
                            })

aanstelling_model = Model("Aanstelling", {
        'regent':  fields.String(description="regent"),
        'regent_ref':  fields.String(description="regent_ref"),
        'college':  fields.String(description="college"),
        'college_ref':  fields.String(description="college_ref"),
        'functie':  fields.String(description="functie"),
        'functie_ref':  fields.String(description="functie_ref"),
        'aanstelling_ref': fields.String(description="aanstelling_ref"),
        'startdate':  fields.String(description="startdate"),
        'start_text':fields.String(description="starty"),
        'enddate':  fields.String(description="enddate"),
        'end_text':fields.String(description="endy")
        })

aanstelling_response = response_model.clone("Aanstelling",
                            {"aanstelling": fields.Nested(aanstelling_model)
                            })

college_model = Model("College", {
        "college": fields.String(description="college"),
        "college_ref":  fields.String(description="college_ref"),
        "period": fields.String(description="period"),
        })

college_response = response_model.clone("College",
                            {"college": fields.Nested(college_model)
                            })

function_model = Model("Function", {
        "function": fields.String(description="functie"),
        "functie_ref":  fields.String(description="functie_ref"),
        "period": fields.String(description="period"),
        })

function_response = response_model.clone("Function",
                            {"function": fields.Nested(college_model)
                            })

period_model = Model("Period", {
        "period": fields.String(description="period"),
        "period_ref":  fields.String(description="period_ref"),
        })

period_response = response_model.clone("Period",
                            {"period": fields.Nested(college_model)
                            })
