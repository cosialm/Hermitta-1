# Placeholder for Vendor Performance Rating API Endpoints
# Actual implementation would use a web framework like Flask or FastAPI

# from ..models.vendor_performance_rating import VendorPerformanceRating
# from ..models.user import User # For updating User.vendor_rating_average, User.vendor_total_ratings_count
# from ..models.maintenance_request import MaintenanceRequest # To check if job is completed by this vendor
# from ..services.vendor_rating_service import calculate_and_update_vendor_average_rating # Conceptual service

# POST /maintenance-requests/{request_id}/vendor-ratings (Submit a rating for a vendor on a specific job)
def submit_vendor_rating_for_maintenance_request(request_id: int):
    # TODO: Implement logic for Landlord/Property Manager to submit a rating for a vendor.
    # 1. Authorize: Ensure current user (Landlord/Staff) can rate for this maintenance_request.
    # 2. Validate request_id: Ensure MaintenanceRequest exists and is in a state that allows rating
    #    (e.g., COMPLETED_CONFIRMED, CLOSED_COMPLETED).
    # 3. Request Body:
    #    - vendor_id: int (User ID of the vendor being rated for this job)
    #    - rating_score: int (e.g., 1-5)
    #    - review_comment: Optional[str]
    # 4. Validation:
    #    - Ensure the specified vendor_id was actually assigned to or worked on this maintenance_request_id.
    #      (e.g., check MaintenanceRequest.resolved_by_user_id or MaintenanceRequestVendorAssignment records).
    #    - Prevent duplicate ratings (e.g., one rating per rated_by_user_id per vendor per request).
    # 5. Logic:
    #    - Create VendorPerformanceRating record with rated_by_user_id from authenticated user.
    #    - Save the rating.
    #    - Trigger recalculation of average rating for the vendor_id:
    #      `calculate_and_update_vendor_average_rating(vendor_id)`
    #      This service function would:
    #        a. Fetch all VendorPerformanceRating records for the vendor.
    #        b. Calculate the new average score and total count.
    #        c. Update User.vendor_rating_average and User.vendor_total_ratings_count for the vendor.
    # 6. Response: Details of the created VendorPerformanceRating or success message.
    pass

# GET /vendors/{vendor_id}/ratings (List all ratings/reviews for a specific vendor)
def list_ratings_for_vendor(vendor_id: int):
    # TODO: Implement logic to list all ratings and reviews for a specific vendor.
    # Potentially public or accessible to Landlords/Staff when selecting vendors.
    # 1. Validate vendor_id: Ensure vendor exists and has VENDOR role.
    # 2. Fetch all VendorPerformanceRating records where vendor_id = vendor_id.
    # 3. Order by rating_date descending.
    # 4. Implement pagination.
    # 5. Response: List of VendorPerformanceRating details (including review_comment, rating_score, rated_by_user_id (can be anonymized like "Landlord L."), rating_date).
    #    Also include the vendor's current average_rating and total_ratings_count from the User model.
    pass

# GET /maintenance-requests/{request_id}/vendor-ratings (List ratings submitted for a specific maintenance request)
def list_ratings_for_maintenance_request(request_id: int):
    # TODO: Implement logic to list ratings associated with a specific maintenance request.
    # Useful for auditing or seeing feedback related to a particular job.
    # 1. Authorize user (Landlord/Staff).
    # 2. Fetch VendorPerformanceRating records where maintenance_request_id = request_id.
    # 3. Response: List of VendorPerformanceRating details.
    pass

# --- Displaying Ratings (Conceptual Notes) ---
#
# 1. Vendor Profile Page (e.g., GET /users/{user_id} where user is a Vendor):
#    - The User model for a VENDOR role now includes `vendor_rating_average` and `vendor_total_ratings_count`.
#    - This endpoint should populate these fields if the user is a vendor.
#    - The profile page could also have a section/tab to display individual reviews (using `GET /vendors/{vendor_id}/ratings`).
#
# 2. Vendor Selection UI (e.g., when assigning a vendor to a Maintenance Request):
#    - When listing available vendors, their `vendor_rating_average` and `vendor_total_ratings_count`
#      should be displayed alongside their name, services, etc.
#    - This allows the landlord/PM to make an informed decision.

# Example (conceptual Flask routes):
# from flask import Blueprint, request, jsonify
# vendor_rating_bp = Blueprint('vendor_ratings', __name__)
#
# @vendor_rating_bp.route('/maintenance-requests/<int:request_id>/vendor-ratings', methods=['POST'])
# def submit_rating_route(request_id):
#     # data = request.get_json() # { vendor_id, rating_score, review_comment }
#     # authenticated_user_id = get_current_user_id()
#     # ... call submit_vendor_rating_for_maintenance_request logic ...
#     return jsonify({"message": "Rating submitted", "rating_id": 1}), 201
#
# @vendor_rating_bp.route('/vendors/<int:vendor_id>/ratings', methods=['GET'])
# def list_vendor_ratings_route(vendor_id):
#     # ... call list_ratings_for_vendor logic ...
#     # vendor_user = User.get_by_id(vendor_id)
#     # return jsonify({
#     #     "vendor_id": vendor_id,
#     #     "average_rating": vendor_user.vendor_rating_average,
#     #     "total_ratings": vendor_user.vendor_total_ratings_count,
#     #     "reviews": [] # List of review details
#     # }), 200
