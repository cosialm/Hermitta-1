import unittest
from datetime import datetime
from models.vendor_performance_rating import VendorPerformanceRating

class TestVendorPerformanceRating(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test VendorPerformanceRating instantiation with only required fields."""
        now = datetime.utcnow()
        rating = VendorPerformanceRating(
            rating_id=1,
            vendor_id=201,
            maintenance_request_id=101,
            rated_by_user_id=301, # e.g., Landlord or Property Manager
            rating_score=5 # e.g., 5 stars
        )

        self.assertEqual(rating.rating_id, 1)
        self.assertEqual(rating.vendor_id, 201)
        self.assertEqual(rating.maintenance_request_id, 101)
        self.assertEqual(rating.rated_by_user_id, 301)
        self.assertEqual(rating.rating_score, 5)
        self.assertIsInstance(rating.rating_score, int)

        # Check defaults
        self.assertIsInstance(rating.rating_date, datetime)
        self.assertTrue((rating.rating_date - now).total_seconds() < 5)
        self.assertIsNone(rating.review_comment)

    def test_instantiation_with_all_fields(self):
        """Test VendorPerformanceRating instantiation with all fields provided."""
        custom_rating_date = datetime(2023, 1, 15, 14, 30, 0)
        rating = VendorPerformanceRating(
            rating_id=2,
            vendor_id=202,
            maintenance_request_id=102,
            rated_by_user_id=302,
            rating_score=4,
            review_comment="Good service, but arrived a bit late.",
            rating_date=custom_rating_date
        )

        self.assertEqual(rating.rating_id, 2)
        self.assertEqual(rating.vendor_id, 202)
        self.assertEqual(rating.maintenance_request_id, 102)
        self.assertEqual(rating.rated_by_user_id, 302)
        self.assertEqual(rating.rating_score, 4)
        self.assertEqual(rating.review_comment, "Good service, but arrived a bit late.")
        self.assertEqual(rating.rating_date, custom_rating_date)
        self.assertIsInstance(rating.rating_date, datetime)

    def test_rating_score_type(self):
        """Test that rating_score is an integer."""
        # This is implicitly tested in the above tests, but can be explicit.
        rating = VendorPerformanceRating(3, 203, 103, 303, rating_score=3)
        self.assertIsInstance(rating.rating_score, int)

        # Test with a different valid score
        rating_low = VendorPerformanceRating(4, 204, 104, 304, rating_score=1)
        self.assertEqual(rating_low.rating_score, 1)


    def test_datetime_field_type(self):
        """Test the type of the datetime field (rating_date)."""
        rating_default_time = VendorPerformanceRating(5, 205, 105, 305, 5)
        self.assertIsInstance(rating_default_time.rating_date, datetime)

        custom_time = datetime(2022, 10, 10, 10, 0, 0)
        rating_custom_time = VendorPerformanceRating(
            rating_id=6, vendor_id=206, maintenance_request_id=106,
            rated_by_user_id=306, rating_score=4, rating_date=custom_time
        )
        self.assertIsInstance(rating_custom_time.rating_date, datetime)
        self.assertEqual(rating_custom_time.rating_date, custom_time)

    # If _calculate_overall_score or other methods were active, they would be tested here.
    # For example, if multi-criteria ratings were active:
    # def test_calculate_overall_score_logic(self):
    #     rating = VendorPerformanceRating(1,1,1,1, rating_score=0) # Placeholder for overall
    #     rating.rating_quality = 5
    #     rating.rating_timeliness = 4
    #     rating.rating_communication = 3
    #     rating.rating_professionalism = None # Test with a None value
    #     # self.assertEqual(rating._calculate_overall_score(), (5+4+3)/3)


if __name__ == '__main__':
    unittest.main()
