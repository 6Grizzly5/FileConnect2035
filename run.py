from app import create_app

app = create_app()

from apscheduler.schedulers.background import BackgroundScheduler

from app.services.auto_dispatch import verifier_guichets

scheduler = BackgroundScheduler()

# WRAPPER
def job_verifier():

    with app.app_context():

        verifier_guichets()

scheduler.add_job(
    job_verifier,
    'interval',
    seconds=15
)

scheduler.start()

if __name__ == '__main__':

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )