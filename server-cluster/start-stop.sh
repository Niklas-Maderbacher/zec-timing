#!/bin/bash

applyall()
{
  kubectl apply $(ls *.yaml | awk ' { print " -f " $1 } ')
}
deleteall()
{
  kubectl delete $(ls *.yaml | awk ' { print " -f " $1 } ')
}