from flask import Flask, jsonify, request
from flask_restful import Resource
from ormgap import Crop, Group, Accession, Country, Project
import re

def is_valid_object_id(value):
    """
    Returns True if `value` is a valid hexadecimal string representation of an ObjectId, False otherwise.
    """
    if not isinstance(value, str):
        return False
    pattern = re.compile("[0-9a-f]{24}")
    return pattern.match(value) is not None

class AccessionsByIDCropProject(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get accessions from database by crop id(s), iso, and project ext_id
        ---
        parameters:
          - name: id
            in: query
            description: Crop id(s)
            required: true
            type: string
            example: 6035f5e5c6be2f14d07d6c7d or 6035f5e5c6be2f14d07d6c7d,6035f5e5c6be2f14d07d6c7e
          - name: iso
            in: query
            description: ISO code of the country
            required: true
            type: string
            example: KE
          - name: project
            in: query
            description: The external project identifier
            required: true
            type: string
            example: "lga" or "bolder"
        responses:
          200:
            description: List of accessions based on provided filters
            schema:
              id: Accession
              properties:
                id:
                  type: string
                  description: Id of the accession
                species_name:
                  type: string
                  description: Name of the species of the accession.
                crop:
                  type: string
                  description: Id of the crop that the accession belongs to.
                landrace_group:
                  type: string
                  description: Id group that the landrace belongs to.
                country:
                  type: string
                  description: Iso2 country to which the accession belongs.
                institution_name:
                  type: string
                  description: Name of the institution that holds the accession.
                source_database:
                  type: string
                  description: Name of the database where the accession was originally stored. Optional.
                latitude:
                  type: float
                  description: Latitude of the geographical location where the accession was collected.
                longitude:
                  type: float
                  description: Longitude of the geographical location where the accession was collected.
                accession_id:
                  type: string
                  description: The identifier of the accession in source database.
                ext_id:
                  type: string
                  description: External identifier for the accession.
                other_attributes:
                  type: dict
                  description: Additional attributes of the accession.
        """
        # Retrieve the parameters
        crop_ids = request.args.get('id')  # Comma separated crop ids
        iso = request.args.get('iso')  # Country iso
        project_ext_id = request.args.get('project')  # Project external id

        # Validate inputs
        if not crop_ids or not iso or not project_ext_id:
            return {'error': 'Crop ID(s), Iso 2, and Project ext_id are required'}, 400
        
        # Convert iso to uppercase and process crop_ids
        iso = iso.upper()
        crop_id_list = list(dict.fromkeys(crop_ids.replace(" ", "").split(',')))

        # Get country by iso
        country = Country.objects(iso_2=iso).first()
        if not country:
            return {"error": f"Country with iso 2 '{iso}' not found"}, 404

        # Get project by ext_id
        project = Project.objects(ext_id=project_ext_id).first()
        if not project:
            return {"error": f"Project with ext_id '{project_ext_id}' not found"}, 404

        # Prepare list to store results
        json_data = []

        for crop_id in crop_id_list:
            if is_valid_object_id(crop_id):
                crop = Crop.objects(id=crop_id).first()
                if crop:
                    # Filter accessions by crop, country, and project
                    accessions = Accession.objects(crop=crop, country=country, project=project)
                    crop_data = {
                        "crop_id": str(crop.id),
                        "accessions": [
                            {
                                "id": str(x.id),
                                "species_name": x.species_name,
                                "ext_id": x.ext_id,
                                "crop": str(x.crop.id),
                                "landrace_group": str(x.landrace_group.id) if x.landrace_group else None,
                                "country": x.country.iso_2,
                                "institution_name": x.institution_name,
                                "source_database": x.source_database,
                                "latitude": x.latitude,
                                "longitude": x.longitude,
                                "accession_id": x.accession_id,
                                "other_attributes": x.other_attributes
                            }
                            for x in accessions
                        ]
                    }
                    json_data.append(crop_data)
                else:
                    json_data.append({"crop_id": crop_id, "error": "Crop not found"})
            else:
                json_data.append({"crop_id": crop_id, "error": "Invalid crop ID"})

        return jsonify(json_data)


class AccessionsByIDCrop(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get accessions from database by crop id(s)
        ---
        parameters:
          - name: id
            in: path
            description: Crop id(s)
            required: true
            type: string
            example: 6035f5e5c6be2f14d07d6c7d or 6035f5e5c6be2f14d07d6c7d,6035f5e5c6be2f14d07d6c7e
        responses:
          200:
            description: 
            schema:
              id: Accession
              properties:
                id:
                  type: string
                  description: Id accession
                species_name: 
                  type: string
                  description: Name of the species of the accession.
                crop: 
                  type: string
                  description: Id crop that the accession belongs to.
                landrace_group:
                  type: string
                  description: Id group that the group belongs to.
                country:
                  type: string
                  description: Iso2 country to which the accession belongs to.
                institution_name: 
                  type: string
                  description: Name of the institution that holds the accession.
                source_database: 
                  type: string
                  description: Name of the database where the accession was originally stored. Optional.
                latitude: 
                  type: float
                  description: Latitude of the geographical location where the accession was collected.
                longitude: 
                  type: float
                  description: Longitude of the geographical location where the accession was collected.
                accession_id:
                  type: string
                  description: The identifier of the accession in source database.
                ext_id: 
                  type: string
                  description: External identifier for the accession.
                other_attributes: 
                  type: dict
                  description: Additional attributes of the accession.
        """
        
        id = request.args.get('id')
        iso = request.args.get('iso')

        print("Ids", id)
        print("iso", iso)

        if id and iso is not None:
            iso = iso.upper()
            id_list = list(dict.fromkeys(id.replace(" ", "").split(',')))
            country = Country.objects(iso_2=iso).first()

            if country is None:
                return {"error": f"Country with iso 2 '{iso}' not found"}, 404

            if len(id_list) == 1:
                if not is_valid_object_id(id_list[0]):
                    return {'error': 'Invalid crop ID'}, 400
                crop = Crop.objects(id=id_list[0]).first()
                if crop is None:
                    return {"error": f"Crop with id {id_list[0]} not found"}, 404
            
            # List of ids provided, list accession for each crop separately
            json_data = []
            for crop_id in id_list:     
                if is_valid_object_id(crop_id):
                    crop = Crop.objects(id=crop_id).first()
                    if crop is None:
                        json_data.append({"error": f"Crop with id {crop_id} not found"})
                    else:
                        accessions = Accession.objects(crop=crop, country=country)
                        crop_data = {"crop_id": str(crop.id),
                                    "accessions": [{"id": str(x.id), "species_name": x.species_name,
                                                    "ext_id": x.ext_id, "crop": str(x.crop.id),
                                                    "landrace_group": str(x.landrace_group.id) if x.landrace_group else None, 
                                                    "country": x.country.iso_2,
                                                    "institution_name":x.institution_name,
                                                    "source_database":x.source_database,
                                                    "latitude":x.latitude,
                                                    "longitude":x.longitude,
                                                    "accession_id":x.accession_id,
                                                    "other_attributes":x.other_attributes}
                                                    for x in accessions]}
                        json_data.append(crop_data)
                else:
                    json_data.append({"crop_id": crop_id,"error": "Invalid crop ID"})
            return json_data
        else: 
            return {'error': 'Crop ID and Iso 2 is required'}, 400
        

class AccessionsByIDGroup(Resource):

    def __init__(self):
        super().__init__()

    def get(self):
        """
        Get accessions from database by group id(s)
        ---
        parameters:
          - name: id
            in: path
            description: Group id(s)
            required: true
            type: string
            example: 6035f5e5c6be2f14d07d6c7d or 6035f5e5c6be2f14d07d6c7d,6035f5e5c6be2f14d07d6c7e
        responses:
          200:
            description: 
            schema:
              id: Accession
              properties:
                id:
                  type: string
                  description: Id accession
                species_name: 
                  type: string
                  description: Name of the species of the accession.
                crop: 
                  type: string
                  description: Id crop that the accession belongs to.
                landrace_group:
                  type: string
                  description: Id group that the group belongs to.
                country:
                  type: string
                  description: Iso2 country to which the accession belongs to.
                institution_name: 
                  type: string
                  description: Name of the institution that holds the accession.
                source_database: 
                  type: string
                  description: Name of the database where the accession was originally stored. Optional.
                latitude: 
                  type: float
                  description: Latitude of the geographical location where the accession was collected.
                longitude: 
                  type: float
                  description: Longitude of the geographical location where the accession was collected.
                accession_id:
                  type: string
                  description: The identifier of the accession in source database.
                ext_id: 
                  type: string
                  description: External identifier for the accession.
                other_attributes: 
                  type: dict
                  description: Additional attributes of the accession.
        """
        
        id = request.args.get('id')
        iso = request.args.get('iso')

        print("Ids", id)
        print("iso", iso)

        if id and iso is not None:            
            iso = iso.upper()
            id_list = list(dict.fromkeys(id.replace(" ", "").split(',')))
            country = Country.objects(iso_2=iso).first()

            if country is None:
                return {"error": f"Country with iso 2 '{iso}' not found"}, 404

            if len(id_list) == 1:
                if not is_valid_object_id(id_list[0]):
                    return {'error': 'Invalid group ID'}, 400
                group = Group.objects(id=id_list[0]).first()
                if group is None:
                    return {"error": f"Group with id {id_list[0]} not found"}, 404
            
            # List of ids provided, list accession for each group separately
            json_data = []
            for group_id in id_list:     
                if is_valid_object_id(group_id):
                    group = Group.objects(id=group_id).first()
                    if group is None:
                        json_data.append({"error": f"Group with id {group_id} not found"})
                    else:
                        accessions = Accession.objects(landrace_group=group, country=country)
                        group_data = {"group_id": str(group.id),
                                    "accessions": [{"id": str(x.id), "species_name": x.species_name,
                                                    "ext_id": x.ext_id, "crop": str(x.crop.id),
                                                    "landrace_group": str(x.landrace_group.id) if x.landrace_group else None, 
                                                    "country": x.country.iso_2,
                                                    "institution_name":x.institution_name,
                                                    "source_database":x.source_database,
                                                    "latitude":x.latitude,
                                                    "longitude":x.longitude,
                                                    "accession_id":x.accession_id,
                                                    "other_attributes":x.other_attributes}
                                                    for x in accessions]}
                        json_data.append(group_data)
                else:
                    json_data.append({"group_id": group_id,"error": "Invalid gropu ID"})
            return json_data
        else: 
            return {'error': 'Group ID and Iso 2 is required'}, 400