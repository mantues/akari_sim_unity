using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine.UI;

public class tcpconnection : MonoBehaviour {
    static UdpClient udp;
    
    // IPEndPoint remoteEP = null;
    // int i = 0;
    private GameObject[] tcptext = new GameObject[2];
    private float[] tcpVal = new float[2];
    
    // light
    private GameObject[] LedLight = new GameObject[2];

    // Use this for initialization
    void Start () {
      int LOCA_LPORT = 50007;
      udp = new UdpClient(LOCA_LPORT);
      udp.Client.ReceiveTimeout = 25;
      // UI
      tcptext[0] = GameObject.Find("Text_tcpvalue");
      // light
      LedLight[0] =  GameObject.Find("Light_2");
   }

   // Update is called once per frame
   void Update (){
      try{
          IPEndPoint remoteEP = null;
          byte[] data = udp.Receive(ref remoteEP);
          string text = Encoding.UTF8.GetString(data);
                    Debug.Log(text);
          tcptext[0].GetComponent<Text>().text = Encoding.UTF8.GetString(data);
          LedLight[0].GetComponent<Light>().intensity = float.Parse(Encoding.UTF8.GetString(data));
      }
      catch(SocketException e){
          Debug.Log("Connection ERROR: \n"+e.ToString());
      }
   }
}
