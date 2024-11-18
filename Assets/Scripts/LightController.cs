using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LightController : MonoBehaviour {

    // light
    private GameObject[] LedLight = new GameObject[2];
    // UI
    private GameObject[] slider = new GameObject[2];
    private float[] sliderVal = new float[2];
    private GameObject[] text = new GameObject[2];
    

    // Use this for initialization
    void Start () {
        // light
        LedLight[0] =  GameObject.Find("Light_0");
        LedLight[1] =  GameObject.Find("Light_1");
        
        // UI
        slider[0] = GameObject.Find("Slider_2");
        slider[1] = GameObject.Find("Slider_3");
        text[0] = GameObject.Find("txLight_0");
        text[1] = GameObject.Find("txLight_1");
        
    }

    // Update is called once per frame
    void Update () {
        //ƒ‰ƒCƒg‚Ì–¾‚é‚³
        sliderVal[0] = slider[0].GetComponent<Slider>().value;
        sliderVal[1] = slider[1].GetComponent<Slider>().value;
        LedLight[0].GetComponent<Light>().intensity = sliderVal[0];
        LedLight[1].GetComponent<Light>().intensity = sliderVal[1];
        // text
        text[0].GetComponent<Text>().text = sliderVal[0].ToString("f2");
        text[1].GetComponent<Text>().text = sliderVal[1].ToString("f2");
    }
}
