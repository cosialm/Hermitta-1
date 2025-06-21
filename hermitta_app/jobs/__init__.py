# This file makes the 'jobs' directory a Python package.

# You can optionally import job functions here if you want to make them
# accessible via from hermitta_app.jobs import some_job_function
# For now, it's kept empty. Callers can import directly from specific modules
# like from hermitta_app.jobs.lease_jobs import process_lease_renewal_reminders_job

# If using a scheduler like APScheduler that's initialized with the app,
# you might import and register jobs here or in create_app().
# For CLI-triggered jobs, this isn't strictly necessary.
