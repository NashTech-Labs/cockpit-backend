PLATFORM_STATE={
    #1000 SERIES IS MAPPED JENKINS PLATFORM
    #KEYS are INT and VALUES are Message String 
    1000:"JENKINS PLATFORM REQUEST ACCEPETED",
    1001:"JENKINS PLATFROM REQUEST IN_PROGRES",
    1002:"JENKINS PLATFROM REQUEST COMPLETED",
    1003:"JENKINS PLATFROM REQUEST IN CREATING EC2 INSTANCE IN_PROGRESS",
    1004:"JENKINS PLATFROM REQUEST IN CREATING EC2 INSTANCE COMPLETED",
    1005:"JENKINS PLATFROM REQUEST IN CREATING GUACAMOLE CONNECTION IN_PROGRESS",
    1006:"JENKINS PLATFROM REQUEST IN CREATING GUACAMOLE CONNECTION COMPLETED",
    1400:"JENKINS PLATFROM REQUEST ERORR",
    1401:"JENKINS PLATFROM REQUEST ERORR IN CREATING EC2 INSTANCE",
    1402:"JENKINS PLATFROM REQUEST ERORR IN DB UPDATE OPERATIONS",
    1403:"JENKINS PLATFROM REQUEST ERORR IN CREATING GUACAMOLE CONNECTION",
    
    #2000 SERIES IS MAPPED KUBERNETES PLATFORM
    2000:"KUBERNETES PLATFROM REQUEST ACCEPETED",
    2001:"KUBERNETES PLATFROM REQUEST IN_PROGRES",
    2002:"KUBERNETES PLATFROM REQUEST COMPLETED",
    2003:"KUBERNETES PLATFROM REQUEST ERORR",

    3000:"KUBERNETES CLUSTER IMPORT ACTION: CLUSTER ALREADRY EXISTS",
    3001:"KUBERNETES CLUSTER IMPORT ACTION: CLUSTER DOSES NOT EXISTS IMPORTING CLUSTER",
    3002:"LIST KUBERNETES CLUSTER PODS",
    3404:"KUBERNETES CLUSTER DOES NOT EXISTS",

    #4000 SERIES IS MAPPED MONITORING
    4000: "MONITORING ENABLE REQUEST ACCEPTED",
    4001: "MONITORING INTIATED INGRESS CONTROLLER DEPLOYMENT",
    4002: "MONITORING SUCCESSFULY DEPOLYED INGRESS CONTROLLER",
    4003: "MONITORING FAILED TO DEPLOY INGRESS CONTROLLER",

    4004: "MONITORING INTIATED PROMETHEUS STACK DEPLOYMENT",
    4005: "MONITORING SUCCESSFULY DEPOLYED PROMETHEUS STACK",
    4006: "MONITORING FAILED TO DEPLOY PROMETHEUS STACK",
    4007: "MONITORING ENABLE REQUEST ACCEPTION FAILED"
    
}
