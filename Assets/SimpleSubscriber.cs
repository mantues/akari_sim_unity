using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

// String Subscriber

public class SimpleSubscriber : MonoBehaviour
{
    ROSConnection ros;
    // Start is called before the first frame update
    void Start()
    {
        ros = ROSConnection.GetOrCreateInstance();
        // Subscriber
        ros.Subscribe<StringMsg>("/simple_topic", ReceiveStringMsg);
    }

    // Update is called once per frame
    void ReceiveStringMsg(StringMsg msg)
    {
        Debug.Log(msg);
    }
}
