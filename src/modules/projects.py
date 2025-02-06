from flask import Flask, jsonify
from flask_restful import Resource
from ormgap import Project

class Projects(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get all projects from database
        ---
        responses:
          200:
            description: 
            schema:
              id: Project
              properties:
                id:
                  type: string
                  description: Project ID
                name:
                  type: string
                  description: Project name
                ext_id:
                  type: string
                  description: External identifier for the project
        """
        q_set = Project.objects()
        json_data = [{"id": str(x.id), "name": x.name, "ext_id": x.ext_id} for x in q_set]
        return json_data
