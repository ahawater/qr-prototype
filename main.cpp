#include <pybind11/embed.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>
#include <chrono>

namespace py = pybind11;

enum CameraType {
    LOWER_CAMERA = 0,
    UPPER_CAMERA = 1
};

void processImageWithPython(const cv::Mat& inputImage, const CameraType cameraType) {

    // Convert cv::Mat to numpy array
    auto img = py::array_t<unsigned char>(
        {inputImage.rows, inputImage.cols, inputImage.channels()},
        inputImage.data
    );
    std::cout << "converted cv::Mat to numpy array" << std::endl;

    //Import qrcodereader module
    py::module_ sys = py::module_::import("sys"); 
    sys.attr("path").attr("append")("../");
    py::module_ script = py::module_::import("qrcodereader");
    std::cout << "imported qrcodereader" << std::endl;

    // Call detect_qr function
    std::cout << "calling detect_qr" << std::endl;
    py::object result = script.attr("detect_qr")(img, static_cast<int>(cameraType));
    std::cout << "called detect_qr" << std::endl;
    py::tuple result_tuple = result.cast<py::tuple>();

    // Process the result and print
    if (cameraType == CameraType::UPPER_CAMERA){
        bool error = result_tuple[0].cast<bool>();
        float u = result_tuple[1].cast<float>();
        std::string detected_code = result_tuple[2].cast<std::string>();
        std::cout << "u: " << u << std::endl;
        std::cout << "Detected QR Code: " << detected_code << std::endl;
        std::cout << "Error: " << (error ? "True" : "False") << std::endl;
    }
    else if (cameraType == CameraType::LOWER_CAMERA){
        std::cout << "Processing upper camera result" << std::endl;
        bool error = result_tuple[0].cast<bool>();
        int x = result_tuple[1].cast<float>();
        int y = result_tuple[2].cast<float>();
        std::string detected_code = result_tuple[3].cast<std::string>();   
        std::cout << "x: " << x << std::endl;
        std::cout << "y: " << y << std::endl;
        std::cout << "Detected QR Code: " << detected_code << std::endl;
        std::cout << "Error: " << (error ? "True" : "False") << std::endl;
    }

}

int main() {
    std::cout << "OpenCV version: " << CV_VERSION << std::endl;
    cv::Mat image = cv::imread("../data/v.12 lower camera crop.jpg");
    if (image.empty()) {
        std::cerr << "Error loading image" << std::endl;
        return -1;
    }
    std::cout << "Image size: " << image.size() << std::endl;

    py::scoped_interpreter guard{};  // Start Python interpreter

    std::cout << "started python interpreter" << std::endl;

    py::module_ np = py::module_::import("numpy");

    std::cout << "imported numpy" << std::endl;

    py::module_ cv2 = py::module_::import("cv2");

    std::cout << "imported cv2" << std::endl;


    for (int i=0; i<5; ++i){
        auto start = std::chrono::high_resolution_clock::now();
        processImageWithPython(image, CameraType::LOWER_CAMERA);
        auto end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duration = end - start;
        std::cout << "Time taken: " << duration.count() << " seconds." << std::endl;
    }
    return 0;
}
