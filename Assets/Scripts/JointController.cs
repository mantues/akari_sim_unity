using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;

namespace AkariPJT{

    public class JointController : MonoBehaviour{
        // Jsondata
        private class AkariData{
            public string message;
            public string timestamp;
            public float pan;
            public float tilt;
            public float light;
            public string text;
        }
        // UDP
       static UdpClient udp;
        // robot
        private GameObject[] joint = new GameObject[2];
        private Vector3[] angle = new Vector3[2];
        // UI
        private GameObject[] slider = new GameObject[3];
        private float[] sliderVal = new float[3];
        private GameObject[] angText = new GameObject[2];
        private GameObject[] udpText = new GameObject[2];
        [SerializeField]Toggle toggle1;
        
        // Start is called before the first frame update
        void Start(){
            // robot
            joint[0] = GameObject.Find("akariservoros");
            joint[1] = GameObject.Find("akariheadros");
            
            // UI
            slider[0] = GameObject.Find("Slider_0");
            slider[1] = GameObject.Find("Slider_1");
            angText[0] = GameObject.Find("Angle_0");
            angText[1] = GameObject.Find("Angle_1");
            udpText[0] = GameObject.Find("Text_modecheck");
            udpText[1] = GameObject.Find("Akaritext");
            toggle1.isOn = PlayerPrefs.GetInt("Toggle")==1?true:false;
            
            // UDP
            int LOCA_LPORT = 50007;
            udp = new UdpClient(LOCA_LPORT);
            udp.Client.ReceiveTimeout = 1000;
            AkariData jsondata = new AkariData();
        }

        // Update is called once per frame
        void Update(){
            // manual mode
            if(!toggle1.isOn){
                //Debug.Log("Manual Mode");
                udpText[0].GetComponent<Text>().text = "Manual Mode";
                // slider
                sliderVal[0] = slider[0].GetComponent<Slider>().value;
                sliderVal[1] = slider[1].GetComponent<Slider>().value;
                angText[0].GetComponent<Text>().text = sliderVal[0].ToString("f2");
                angText[1].GetComponent<Text>().text = sliderVal[1].ToString("f2");
                // Vector
                angle[0].z = sliderVal[0];
                angle[1].x = sliderVal[1];
                // MoveJoint
                joint[0].transform.localEulerAngles = angle[0];
                joint[1].transform.localEulerAngles = angle[1];
                
            }
            // tcp connection mode
            else{
                //Debug.Log("TCP Mode");
                udpText[0].GetComponent<Text>().text = "TCP Mode";
                try{
                    IPEndPoint remoteEP = null;
                    byte[] data = udp.Receive(ref remoteEP);
                    string jsonString = System.Text.Encoding.UTF8.GetString(data);
                    AkariData akaridata = JsonUtility.FromJson< AkariData >( jsonString );
                              Debug.Log(akaridata.message+" : "+akaridata.timestamp
                              +",Pan : "+akaridata.pan
                              +",Tilt : "+akaridata.tilt
                              +",Light : "+akaridata.light
                              +",Text : "+akaridata.text);
                    // Vector
                    angle[0].z = float.Parse(akaridata.pan.ToString());
                    angle[1].x = float.Parse(akaridata.tilt.ToString());
                    // MoveJoint
                    joint[0].transform.localEulerAngles = angle[0];
                    joint[1].transform.localEulerAngles = angle[1];
                    udpText[1].GetComponent<Text>().text = akaridata.text;
                }
                catch(SocketException e){
                    Debug.Log("Connection ERROR: \n"+e.ToString());
                }
            }

            
        }
    }

}
