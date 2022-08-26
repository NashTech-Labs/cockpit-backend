{
    "apiVersion": "argoproj.io/v1alpha1",
    "kind": "Application",
    "metadata": {
        "name": "nginxdeployment",
        "namespace": "argocd"
    },
    "spec": {
        "project": "default",
        "source": {
            "repoURL": "https://github.com/Balraj0017/Nginx_deployment.git",
            "targetRevision": "HEAD",
            "path": "."
        },
        "destination": {
            "server": "https://kubernetes.default.svc",
            "namespace": "myapp"
        },
        "syncPolicy": {
            "syncOptions": [
                "CreateNamespace=true"
            ],
            "automated": {
                "selfHeal": true,
                "prune": true
            }
        }
    }
}