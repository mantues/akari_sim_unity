using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;


/// String publisher

public class SimplePublisher : MonoBehaviour
{
    ROSConnection ros;
    float publishMessageFrequency = 1f;
    float timeElapsed;
    
    // Start is called before the first frame update
    void Start()
    {
          ros = ROSConnection.GetOrCreateInstance();
          // Publisher
          ros.RegisterPublisher<StringMsg>("/simple_topic");
    }

    // Update is called once per frame
    void Update()
    {
        timeElapsed += Time.deltaTime;
        // Publish
        if (timeElapsed > publishMessageFrequency)
        {
          StringMsg msg = new StringMsg();
          var dt = DateTime.Now;
          msg.data = String.Format("{0}:{1}:{2}", new string[] {dt.Hour.ToString(), dt.Minute.ToString(), dt.Second.ToString()});
          ros.Publish("/simple_topic", msg);
          timeElapsed = 0;
          }
    }
}
