# Cloud Computing Term Project on IaaS cloud middleware

* Project statement:
    * Create a cloud environment with a number of servers, allowing users to submit their jobs, scale their jobs
    * Make simple resource management solutions in determining where to place a VM and when to migrate them

* Project steps
    * Cloud environment setup
        * Set up the KVM environment
        * Provide an interface for job submission and scaling
    * Middleware implementation
        * Explore libvirt to achieve VM creation, scaling, and migration
        * Study and summarize papers in VM placement
        * Design and develop a VM placement and migration decision algorithm
    * System monitoring
        * Install one of the cloud monitoring system to observe various behaviors of the system
        * Continuously display memory load, CPU load, IO load, etc.
        * For individual VMs, individual nodes, etc.
        * Create the interface for the monitoring result display
        * Obtain cloud workloads, and perform cloud middleware management
    * Analyze the results

* Papers to refer:
  * D. Ardagna, M. Trubian, and L. Zhang, “SLA based resource allocation policies in autonomic environments,” Journal of Parallel and Distributed Computing, vol. 67, pp. 259-270, 2007.
  * J. Almeida, V. Almeida, D. Ardagna, Í. Cunha, C. Francalanci, and M. Trubian, “Joint admission control and resource allocation in virtualized servers,” Journal of Parallel and Distributed Computing, vol. 70, pp. 344-362, 2010.
  * On Theory of VM Placement: Anomalies in Existing Methodologies and Their Mitigation Using a Novel Vector Based Approach
  * On Resource Management for Cloud Users: A Generalized Kelly Mechanism Approach
  * SLA-aware virtual resource management for cloud infrastructures
  * VMware Distributed Resource Management: Design, Implementation, and Lessons Learned
  * Q-Clouds: Managing Performance Interference Effects for QoS-Aware Clouds
