from datetime import datetime
from typing import Optional

# Assuming User model exists in models.user
# Assuming MaintenanceRequest model exists in models.maintenance_request

class VendorPerformanceRating:
    def __init__(self,
                 rating_id: int, # PK
                 vendor_id: int, # FK to User (where User.role == VENDOR)
                 maintenance_request_id: int, # FK to MaintenanceRequest, context of the rating
                 rated_by_user_id: int, # FK to User (e.g., Landlord, Property Manager)
                 rating_score: int, # Overall score, e.g., 1 to 5 stars
                 # Optionally, could have multiple rating criteria:
                 # rating_quality: Optional[int] = None, # Score for quality of work
                 # rating_timeliness: Optional[int] = None,
                 # rating_communication: Optional[int] = None,
                 # rating_professionalism: Optional[int] = None,
                 review_comment: Optional[str] = None, # Text review
                 rating_date: datetime = datetime.utcnow()):

        self.rating_id = rating_id
        self.vendor_id = vendor_id
        self.maintenance_request_id = maintenance_request_id
        self.rated_by_user_id = rated_by_user_id
        self.rating_score = rating_score # This is the overall score for now

        # Example for multi-criteria if expanded later:
        # self.rating_quality = rating_quality
        # self.rating_timeliness = rating_timeliness
        # self.rating_communication = rating_communication
        # self.rating_professionalism = rating_professionalism
        # self.rating_score = self._calculate_overall_score() # If overall is derived

        self.review_comment = review_comment
        self.rating_date = rating_date

    # def _calculate_overall_score(self) -> Optional[float]:
    #     """ Example: Calculates an average if multiple criteria are used. """
    #     scores = [s for s in [self.rating_quality, self.rating_timeliness,
    #                            self.rating_communication, self.rating_professionalism] if s is not None]
    #     if not scores:
    #         return None
    #     return sum(scores) / len(scores)

# Example Usage:
# rating1 = VendorPerformanceRating(
#     rating_id=1,
#     vendor_id=51, # Vendor User ID
#     maintenance_request_id=101, # Associated Maintenance Request ID
#     rated_by_user_id=10, # Landlord User ID
#     rating_score=5, # 5 stars overall
#     review_comment="Excellent work, very prompt and professional."
# )
# print(f"Rating for Vendor {rating1.vendor_id} on Request {rating1.maintenance_request_id}: {rating1.rating_score} stars.")
