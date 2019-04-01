# Facial Recognition Proof of Concept POC

In this project we created a facial recognition system using Docker and Kubernetes to deploy the models intp production.

### Models:

* Facial Recognition - Pytorch [VGGFace2](http://www.robots.ox.ac.uk/~albanie/pytorch-models.html)
* Face Detection - Caffee [SSD](https://github.com/thegopieffect/computer_vision/tree/master/CAFFE_DNN)

## Dashboard:

To run the dashboard, make sure you change create a MySQL DB, change the credentials in the script and use:

```
python dash_server.py
```