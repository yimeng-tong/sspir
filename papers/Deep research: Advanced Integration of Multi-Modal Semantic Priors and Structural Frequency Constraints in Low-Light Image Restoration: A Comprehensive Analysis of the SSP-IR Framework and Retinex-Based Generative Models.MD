Advanced Integration of Multi-Modal Semantic Priors and Structural Frequency Constraints in Low-Light Image Restoration: A Comprehensive Analysis of the SSP-IR Framework and Retinex-Based Generative Models
The technological evolution of image restoration has transitioned from localized, heuristic-based pixel manipulation to complex, prior-guided generative frameworks capable of high-level scene understanding and structural reconstruction. Among the most challenging sub-tasks in this field is low-light image enhancement (LLIE), where the degradation involves a non-linear confluence of underexposure, sensor noise, and the loss of structural detail.[1, 2] The emergence of the Semantic and Structure Priors for Diffusion-based Realistic Image Restoration (SSP-IR) framework represents a watershed moment in addressing these challenges by combining Multimodal Large Language Models (MLLMs), Contrastive Language-Image Pre-training (CLIP) architectures, and Fast Fourier Transform (FFT) constraints.[3, 4] This analysis explores the technical architecture of SSP-IR, investigates the synergy between the classical Retinex theory and modern diffusion models, and synthesizes current research at the intersection of semantic comprehension and low-light restoration.
Theoretical Underpinnings of Low-Light Image Enhancement
Image restoration (IR) aims to recover a high-quality (HQ) latent image from a low-quality (LQ) counterpart affected by environmental or hardware-induced degradations.[3] Low-light enhancement is a specifically ill-posed inverse problem because the "hidden" signal in dark regions is often dominated by stochastic noise, rendering traditional spatial filters inadequate for retrieving visually pleasing and semantically accurate results.[5, 6]
The historical trajectory of LLIE began with global adjustment techniques such as Histogram Equalization (HE) and Gamma Correction.[7, 8] While efficient, these methods operate without context, often leading to over-exposure in bright areas and the amplification of artifacts in shadows.[1, 7] The field progressed toward data-driven Convolutional Neural Networks (CNNs) and Transformers, which learn mappings from paired datasets (e.g., LOL, UHD-LL).[9, 10, 11] However, these discriminative models often suffer from over-smoothing or the generation of "plastic" textures.[12, 13] The current frontier utilizes Denoising Diffusion Probabilistic Models (DDPMs), which formulate restoration as a controllable generation process, leveraging rich image priors learned from billions of image-text pairs.[3, 4, 14]
Architectural Deep Dive into the SSP-IR Framework
The SSP-IR framework addresses the fundamental inability of existing diffusion models to fully exploit information from severely degraded images.[3, 15] It operates on the principle that realistic restoration requires two types of guidance: what the image means (semantic prior) and how the image is arranged (structure prior).[4, 15]
Multi-Modal Semantic Prior Extraction
The semantic prior in SSP-IR is unique for its "explicit-implicit" collaboration strategy, which utilizes both the linguistic reasoning of MLLMs and the visual representations of CLIP.[4]
Explicit Branch (MLLM): High-level visual understanding is provided by an MLLM (such as IDEFICS or LLaVA), which analyzes the LQ image to generate textual descriptions.[16, 17] These descriptions are not merely captions but inferential observations about the scene's content, potential lighting conditions, and restoration targets.[16, 18] These textual prompts are mapped into a latent space via the CLIP text encoder to form "restored text embeddings".[4] A key advantage noted in the literature is that these explicit priors allow for user intervention; a user can modify the prompt to adjust the restoration style or focus on specific semantic elements.[3]
Implicit Branch (CLIP/Refine Layer): Recognizing that text cannot capture every nuance of an image, an implicit branch uses a CLIP image encoder to extract high-dimensional visual features.[4, 19] To prevent the model from inheriting noise from the LQ input, a specialized "Refine Layer" is employed to correct the image embedding, effectively filtering out degradation-induced features while retaining intrinsic semantic cues.[4]
Structure Prior and the Constrained Processor
To handle structural fidelity, SSP-IR introduces a dedicated module known as the Processor, which is designed to be degradation-independent.[4, 13] This is critical because structural artifacts in low-light images (such as ringing or blocking) can be misinterpreted by diffusion models as valid textures.[6] The Processor is supervised by two distinct losses:
RGB Constraint: This ensures spatial alignment and pixel-level consistency between the extracted features and the input scene.[4, 15]
FFT Constraint: The Fast Fourier Transform constraint is vital for global modeling. By supervising the feature extraction in the frequency domain, the framework ensures that the global distribution of energy (lightness) and the periodic patterns of the scene (edges and textures) are preserved.[4, 20]
The extracted structure features are integrated into the denoising U-Net through a ControlNet architecture, providing a spatial "skeleton" that guides the generation of high-frequency details.[4, 21]
Multi-Level Attention Integration
The final component of SSP-IR is a multi-level attention mechanism that fuses the explicit/implicit semantic embeddings and the structural control features into the diffusion process.[4, 15] This allows the model to balance the "hallucination" capabilities of the diffusion backbone with the factual constraints of the input priors.[3]
Retinex Theory and Its Integration with Generative Frameworks
Retinex theory remains the most influential physical model for low-light enhancement, providing a principled foundation for decomposing an image I into reflectance R and illumination L components: I=R⊙L.[6, 8, 22]
Retinex-Driven Diffusion Models
Modern research has successfully integrated Retinex rules as "plug-and-play" modules within diffusion backbones. A prominent example is the Diff-Retinex++ framework, which leverages the generative power of diffusion models to reconstruct Retinex components.[23]
Mechanism: Instead of direct pixel-to-pixel mapping, Diff-Retinex++ treats the enhancement of R and L as two separate sub-problems.[23] It uses a Retinex-Driven Supervision Attention Module (R-SAM) to learn Retinex rules in the latent space of the network.[23]
Benefits: This coupling allows the model to benefit from the powerful generation ability of diffusion models while adhering to the physical constraints of light transport, resulting in better removal of information loss in extreme darkness.[23]
Zero-Shot Personalized Enhancement (RetinexGDP)
Another significant advancement is RetinexGDP, which demonstrates how Retinex theory can be combined with CLIP for zero-shot personalization.[24]
Mechanism: The model performs a zero-shot Retinex decomposition using a Gaussian convolutional layer to separate reflectance.[24] This reflectance component is then used as a condition for the Denoising Diffusion Implicit Model (DDIM) sampling process.[24]
CLIP Integration: The CLIP model is introduced to guide the sampling based on user-provided text instructions.[24] This allows for "personalized" low-light enhancement, where the user can specify the desired "look" (e.g., "warm lighting," "high contrast") while the Retinex prior ensures the content remains faithful to the original scene.[24]
The Reti-Diff Framework
A recently highlighted work, Reti-Diff (ICLR 2025), proposes a Retinex-based Latent Diffusion Model.[25] It utilizes a compact latent space to extract reflectance and illumination priors, which are then used by a "Retinex-guided Transformer" (RGformer) to guide the decomposition of image features.[25] This approach solves the pixel misalignment issues common in traditional multi-stage Retinex pipelines by operating entirely within the latent domain.[25]
Synergy: Applying Retinex Theory within the SSP-IR Framework
For optimizing low-light scenes, the SSP-IR framework can be enhanced by adopting Retinex-inspired modularity. The following table outlines how Retinex principles can be integrated into the specific components of SSP-IR.
SSP-IR Component
Retinex Integration Strategy
Expected Benefit
MLLM Semantic Prior
Provide Retinex-decomposed Reflectance (R) as the visual prompt to the MLLM.
More accurate scene descriptions since R is illumination-invariant.
CLIP Image Embedding
Extract implicit features from the Illumination map (L) to guide global tone.
Better control over non-uniform lighting and exposure correction.
FFT Structural Prior
Apply FFT constraints specifically to the Reflectance features.
Enhanced edge preservation and detail retrieval without noise interference.
Diffusion Sampling
Use a Retinex-aware loss function (L 
total
​
 =L 
DDM
​
 +L 
RMoE
​
 ).
Physical consistency in lighting restoration and artifact suppression.
[3, 4, 23, 24]
By pre-decomposing the input image, the SSP-IR Processor can extract structural features from the reflectance component, which is naturally clearer than the raw underexposed image.[5, 23] Simultaneously, the MLLM can use the estimated illumination map to "understand" the specific type of lighting degradation (e.g., "backlit indoor scene") and generate a more precise "restored text embedding".[16, 18]
Semantic-Aware Research in Low-Light Scenarios
The move toward "semantic-aware" restoration stems from the observation that global, homogeneous adjustments often lead to region-specific artifacts—such as turning a black car gray or losing texture in the sky.[26, 27, 28]
The SKF Framework and Multi-Color Space Learning
The Semantic-Aware Knowledge-Guided Framework (SKF) is a representative state-of-the-art method in this category.[26, 27] It introduces three pivotal mechanisms:
Semantic Feature Enhancement (SE) Module: This module performs pixel-wise interaction between image features and features from a frozen Semantic Knowledge Bank (SKB, e.g., HRNet).[27] It uses a transposed-attention mechanism to compute semantic awareness, allowing the network to apply different enhancement strategies for different object classes.[27]
Semantic-Guided Color Histogram (SCH) Loss: Traditional color losses are global. SCH loss segments the image into instances using semantic maps and enforces color consistency for each instance separately.[26, 29] This is particularly effective for maintaining the "naturalness" of object colors under extreme lighting.[29]
Semantic-Guided Adversarial (SA) Loss: This uses semantic priors to guide the discriminator in identifying "fake" textures in specific regions, leading to more realistic detail recovery.[27]
Causal Inference and Semantic Consistency (CWNet)
Recent work like CWNet proposes a Structural Causal Model (SCM) for LLIE.[28] The core objective is to maintain consistency in "causal factors," where semantic information is seen as the underlying cause of the image content.[28] CWNet utilizes CLIP to ensure that the semantic meaning of the enhanced image matches the original, even if the pixel values change significantly.[28]
Agentic Restoration and Autonomous Workflows
A rising trend involves using MLLMs not just as feature providers, but as autonomous agents that control the restoration pipeline.[25, 30]
RestoreAgent: This framework finetunes an MLLM to serve as a perception and planning agent.[30] It can analyze a low-light image, identify mixed degradations (e.g., noise + blur + darkness), and "plan" a step-by-step restoration using various specialized tools.[30]
AgenticIR: Similar to RestoreAgent, it uses statistical experience to guide an LLM in selecting the most effective execution sequences for tool usage, improving the quality and consistency of recovered results.[30]
Frequency-Domain Optimization and Structural Priors
The integration of FFT into restoration frameworks like SSP-IR is justified by the "amplitude-phase" duality of the Fourier spectrum.[6] In the frequency domain, the amplitude ∣F(x)∣ encodes the global illumination and contrast, while the phase ∠F(x) encodes the local structure and arrangement of pixels.[6, 31, 32]
Dual-Domain Networks (AFMNet and FSIDNet)
Research has shown that pure spatial mappings struggle to balance brightness and detail fidelity.[33] Dual-domain networks address this by processing information in both the spatial and frequency domains.[34, 35]
AFMNet: This model uses a Multi-Scale Amplitude Estimator (MSAE) to adaptively boost the suppressed amplitude components of low-light images.[33, 36] It employs a Frequency-Modulated Attention Block (FMAB) that injects spectral modulation as a prior into the attention mechanism, allowing for targeted information compensation in regions with high energy loss.[33]
FSIDNet: A two-stage architecture where the first stage restores amplitude (lightness) and the second stage restores phase (structure).[37] This staged approach is highly effective because it treats illumination and detail as complementary but distinct restoration tasks.[37, 38]
FFT Loss and Degradation Disentanglement
The use of FFT loss, as seen in SSP-IR and FECNet, is based on the insight that certain degradations (like flares or rain) manifest uniquely in the frequency domain.[32, 39, 40] FFT allows for a global receptive field at a low computational cost, enabling the model to "see" the relationship between all points in the image simultaneously.[39, 40] This is particularly useful for low-light enhancement, where the "correct" brightness of a pixel may depend on the global illumination context of the entire scene.[6]
Benchmark Datasets and Quantitative Comparisons
Developing semantic-aware low-light models requires datasets that go beyond simple image pairs. The following table compares common datasets used in the field.
Dataset
Images
Degradation Type
Annotation Level
Primary Application
LOL (v1/v2)
1000+
Real Low-Light
Pixel-paired
General Enhancement
MIT-Adobe FiveK
5000
Expert-Retouched
Categorical tags
Aesthetic adjustment
ExDark
7363
Real Low-Light
Object Bounding Boxes
Low-light Detection
UHD-LL
2150
4K Real Low-Light
Pixel-paired
Ultra-HD Enhancement
LIDQ
10k+
Enhanced
Artifact MOS
Quality Assessment
N2UD
3201
Underwater Blur
Pixel-paired
Multi-modal Enhancement
[9, 41, 42, 43, 44]
Quantitative metrics for these tasks often include Full-Reference (FR) metrics like PSNR and SSIM, but for semantic fidelity, researchers increasingly rely on No-Reference (NR) metrics and Perceptual metrics like LPIPS (Learned Perceptual Image Patch Similarity).[3, 14] For example, SSP-IR has demonstrated superiority in SSIM (Structural Similarity) on real-world datasets, which is attributed to its strong FFT-based structure prior.[3, 4]
Implementation Strategy for a Hybrid SSP-IR Framework
For a researcher seeking to implement a Retinex-optimized SSP-IR framework, the following technical pathway is suggested by the literature:
Decomposition Stage: Utilize a pre-trained, lightweight Retinex decomposition network (e.g., from RetinexNet or RUAS) to generate the initial reflectance (R) and illumination (L) maps.[11, 45]
Semantic Extraction:
Feed the reflectance map R into an MLLM (e.g., IDEFICS) to generate descriptions that are un-distorted by poor lighting.[16, 18]
Feed the illumination map L into a CLIP-based encoder to capture the global "atmosphere" of the scene.[17, 28]
Structural Processing:
Pass the reflectance map through the SSP-IR Processor with FFT and RGB constraints.[4]
Since R contains the edges and textures without the "fog" of underexposure, the extracted structure prior will be significantly more accurate.[5, 22]
Generative Denoising:
Use a pre-trained Stable Diffusion model as the backbone.[3, 4]
Inject the semantic embeddings and structural ControlNet features into the denoising steps.[15]
Incorporate a "Retinex-Consistency" loss that penalizes the model if the enhanced image I 
out
​
  cannot be decomposed back into a version of the original reflectance R.[23]
Conclusion and Future Outlook
The field of low-light image enhancement is rapidly moving away from simple "brightening" toward a nuanced reconstruction of reality. The SSP-IR framework, by integrating multi-modal semantic priors and frequency-domain structural constraints, offers a robust solution to the "hallucination" problem inherent in generative models.[3, 4] The synthesis of Retinex theory into these generative workflows provides the necessary physical anchoring, ensuring that enhanced images are not only visually pleasing but also physically and semantically consistent with the original scene.[23, 24, 25]
Future research is expected to focus on "Autonomous Diffusion" and "Agent-based Restoration," where models can zero-shot adapt to unknown degradations by reasoning about the image's content and lighting environment in real-time.[14, 30, 46] Furthermore, the adaptation of these models to Ultra-HD (4K/8K) and video sequences remains a critical challenge, requiring advancements in parameter-efficient fine-tuning (PEFT) and latent-space acceleration.[14, 25, 44] As these technologies mature, the "black box" of low-light imaging will transform into an interpretable, controllable, and high-fidelity medium for digital photography and industrial vision.
--------------------------------------------------------------------------------
Retinex-Based Low-Light Image Enhancement via Spatial-Channel Redundancy Compression and Joint Attention - MDPI, https://www.mdpi.com/2079-9292/14/11/2212
LLIE Models: Advances in Low-Light Enhancement - Emergent Mind, https://www.emergentmind.com/topics/low-light-image-enhancement-llie-models
SSP-IR: Semantic and Structure Priors for Diffusion-based Realistic Image Restoration, https://arxiv.org/html/2407.03635v2
SSP-IR: Semantic and Structure Priors for Diffusion-based Realistic ..., https://zyhrainbow.github.io/projects/SSP-IR/
Low-light Image Enhancement with Retinex Decomposition in Latent Space - arXiv, https://arxiv.org/html/2603.15131v1
Low-Light Image Enhancement (LLIE) - Emergent Mind, https://www.emergentmind.com/topics/low-light-image-enhancement-llie
Low-Light Image Enhancement Based on Retinex Theory and Attention Mechanism, https://www.researchgate.net/publication/390016244_Low-Light_Image_Enhancement_Based_on_Retinex_Theory_and_Attention_Mechanism
Retinex-based low-light image enhancement with logarithmic color correction - SPIE Digital Library, https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13457/3053801/Retinex-based-low-light-image-enhancement-with-logarithmic-color-correction/10.1117/12.3053801.full
NTIRE 2025 Challenge on Low Light Image Enhancement: Methods and Results - arXiv, https://arxiv.org/html/2510.13670v1
Larger Hausdorff Dimension in Scanning Pattern Facilitates Mamba-Based Methods in Low-Light Image Enhancement - Preprints.org, https://www.preprints.org/manuscript/202511.1086
[PDF] Frequency-Spatial Interaction Driven Network for Low-Light ..., https://www.semanticscholar.org/paper/Frequency-Spatial-Interaction-Driven-Network-for-Tao-Tao/cb521c678645d8add5f8e7e4499f20d8f9c48951
Daily Papers - Hugging Face, https://huggingface.co/papers?q=generative%20texture%20restoration%20network
Qualitative results on the USR-248 dataset (×4 and ×8 scale), which... - ResearchGate, https://www.researchgate.net/figure/Qualitative-results-on-the-USR-248-dataset-4-and-8-scale-which-compare-our-FSN-with_fig3_378345105
Diffusion Models for Low-Light Image Enhancement A Multi-Perspective Taxonomy and Performance Analysis - arXiv, https://arxiv.org/html/2510.05976v1
SSP-IR: Semantic and Structure Priors for Diffusion-Based Realistic ..., https://ieeexplore.ieee.org/document/10870312/
arXiv:2401.11401v1 [cs.CV] 21 Jan 2024, https://arxiv.org/pdf/2401.11401
QLIP: A Dynamic Quadtree Vision Prior Enhances MLLM Performance Without Retraining, https://openreview.net/forum?id=DSq3r8PjpQ
LLMRA: Multi-modal Large Language Model based Restoration Assistant - arXiv, https://arxiv.org/html/2401.11401v1
Dual-Head Fusion Network for Image Enhancement | Request PDF - ResearchGate, https://www.researchgate.net/publication/371288452_Dual-Head_Fusion_Network_for_Image_Enhancement
A Dual-Domain Deep Convolutional Variational Autoencoder Framework for Unsupervised Structural Health Monitoring Using Vision-Based Vibration Analysis | Journal of Computing in Civil Engineering - ASCE Library, https://ascelibrary.org/doi/10.1061/JCCEE5.CPENG-7116
One-step diffusion-based real-world image super-resolution with visual perception distillation | Request PDF - ResearchGate, https://www.researchgate.net/publication/400765166_One-step_diffusion-based_real-world_image_super-resolution_with_visual_perception_distillation
ILR-Net: Low-light image enhancement network based on the combination of iterative learning mechanism and Retinex theory - Our journal portfolio - PLOS, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314541
Diff-Retinex++: Retinex-Driven Reinforced Diffusion Model for Low ..., https://www.computer.org/csdl/journal/tp/2025/08/10974676/269aNZrD5Ze
Zero-shot Text-based Personalized Low-Light Image Enhancement ..., https://openreview.net/forum?id=GUd6zTrTBb
ChunmingHe/awesome-multimodal-large-language ... - GitHub, https://github.com/ChunmingHe/awesome-multimodal-large-language-models-in-low-level-vision
Semantic-Aware Low-Light Image Enhancement by Learning from Multiple Color Spaces, https://www.mdpi.com/2076-3417/15/10/5556
CVPR Poster Learning Semantic-Aware Knowledge Guidance for ..., https://cvpr.thecvf.com/virtual/2023/poster/23203
CWNet: Causal Wavelet Network for Low-Light Image Enhancement - CVF Open Access, https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_CWNet_Causal_Wavelet_Network_for_Low-Light_Image_Enhancement_ICCV_2025_paper.pdf
(PDF) Semantic-Aware Low-Light Image Enhancement by Learning from Multiple Color Spaces - ResearchGate, https://www.researchgate.net/publication/391790502_Semantic-Aware_Low-Light_Image_Enhancement_by_Learning_from_Multiple_Color_Spaces
RestoreAgent: Autonomous Image Restoration Agent via Multimodal Large Language Models | Request PDF - ResearchGate, https://www.researchgate.net/publication/397202537_RestoreAgent_Autonomous_Image_Restoration_Agent_via_Multimodal_Large_Language_Models
Restoring extremely low-light light fields via decomposition-enhancement and frequency-pixel fusion - Optica Publishing Group, https://opg.optica.org/oe/fulltext.cfm?uri=oe-33-3-3697
OSMamba: Omnidirectional Spectral Mamba with Dual-Domain Prior Generator for Exposure Correction - arXiv, https://arxiv.org/html/2411.15255v1
AFMNet: A Dual-Domain Collaborative Network with Frequency ..., https://pmc.ncbi.nlm.nih.gov/articles/PMC12731650/
HVI-Based Spatial–Frequency-Domain Multi-Scale Fusion for Low-Light Image Enhancement - MDPI, https://www.mdpi.com/2076-3417/15/19/10376
DiffDark: Multi-prior integration driven diffusion model for low-light image enhancement | Request PDF - ResearchGate, https://www.researchgate.net/publication/391872319_DiffDark_Multi-prior_integration_driven_diffusion_model_for_low-light_image_enhancement
AFMNet: A Dual-Domain Collaborative Network with Frequency Prior Guidance for Low-Light Image Enhancement - MDPI, https://www.mdpi.com/1099-4300/27/12/1220
Frequency-Spatial Interaction Driven Network for Low-Light Image Enhancement - arXiv, https://arxiv.org/html/2510.22154v1
[2510.22154] Frequency-Spatial Interaction Driven Network for Low-Light Image Enhancement - arXiv, https://arxiv.org/abs/2510.22154
When Fast Fourier Transform Meets Transformer for Image Restoration - European Computer Vision Association, https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/06190.pdf
Integrating Spatial and Frequency Information for Under-Display Camera Image Restoration, https://arxiv.org/html/2501.18517v1
Progressive Multi-Scale Perception Network for Non-Uniformly Blurred Underwater Image Restoration - MDPI, https://www.mdpi.com/1424-8220/25/17/5439
Unified UHD Image Restoration with Progressive Frequency Learning and Degradation-aware Prompts Supplementary Mat, https://openaccess.thecvf.com/content/CVPR2025/supplemental/Liu_UHD-processer_Unified_UHD_CVPR_2025_supplemental.pdf
Qualitative and Quantitative Quality Assessment of Low-Light Enhanced Images: A Dataset and Benchmark Metric | OpenReview, https://openreview.net/forum?id=FwtgOQvMol
FLOL: Fast Baselines for Real-World Low-Light Enhancement - arXiv.org, https://arxiv.org/html/2501.09718v2
Frequency-domain loss function for deep exposure correction of dark images - PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC8549936/
LD-RPS: Zero-Shot Unified Image Restoration via Latent Diffusion Recurrent Posterior Sampling - CVF Open Access, https://openaccess.thecvf.com/content/ICCV2025/papers/Li_LD-RPS_Zero-Shot_Unified_Image_Restoration_via_Latent_Diffusion_Recurrent_Posterior_ICCV_2025_paper.pdf