from prometheus_client import Histogram, Counter

LATENCY = Histogram('latency', 
                    'the amount of time that it takes to process one request', 
                    labelnames = ['endpoint', 'status_code'],
                    namespace = 'ghost_job_detector',
                    unit='seconds')

REQUESTS_NUMBER = Counter('requests_number',
                          'the number of timese that this endpoint has been called',
                          labelnames = ['endpoint', 'status_code'],
                          namespace='ghost_job_detector'
                        )

FAILED_REQUESTS = Counter('failed_requests',
                        'the number of times that the request failed',
                        labelnames=['endpoint', 'status_code', 'error'],
                        namespace='ghost_job_detector'
                        )

DEPENDENCY_ERRORS = Counter('dependency_errors',
                        'the number of times that the request failed',
                        labelnames=['service', 'operation', 'error'],
                        namespace='ghost_job_detector'
                        )

DEPENDENCY_LATENCY = Histogram('dependency_latency',
                        'the amount of latency that dependencies take when doing operations',
                        labelnames=['service', 'operation', 'status'],
                        namespace='ghost_job_detector')