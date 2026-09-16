# Next-Generation Architectures for Geometric Image Editing: Beyond In-Plane Manipulation

The domain of geometric image editing—defined as the task of repositioning, scaling, or rotating an object within a single image while preserving global scene coherence and realism—has experienced a paradigm shift driven by the generative priors of diffusion models. Early approaches to image manipulation largely relied on generative adversarial networks or explicit 3D modeling, which often suffered from limited generalization or required multi-view data. The advent of large-scale diffusion models introduced robust semantic priors, allowing for single-image editing through textual guidance, latent inversion, and attention manipulation. Recent training-free frameworks have demonstrated that geometric image editing can be effectively managed by decoupling the process into distinct, sequential subtasks: object transformation, source region inpainting, and target region refinement. This decoupled architecture mitigates the competing demands inherent in single-step optimization frameworks, where preserving the background often conflicts with generating newly exposed object surfaces.

Despite these architectural advancements, exhaustive empirical evaluations and metric-driven diagnostics indicate that current state-of-the-art training-free models have reached an intrinsic structural ceiling. While in-plane manipulations such as translation and minor scaling are functionally solved, significant degradation in subject-structural fidelity occurs during large-angle three-dimensional out-of-plane rotations and severe scaling operations. Current frameworks rely heavily on monocular depth estimation and purely two-dimensional in-plane attention mechanisms, which physically distort depth cues and occlude structural semantics when mapped onto a 2D plane.

This comprehensive report establishes an architectural and experimental roadmap designed to transcend the limitations of current two-dimensional geometric editing paradigms. Rooted in an exhaustive diagnostic analysis of existing frameworks, the ensuing sections propose four major experimental directions. The first direction explores Single-Image Novel-View Synthesis for robust out-of-plane editing, advocating a transition from depth-based point cloud reprojection to pixel-splatting and video diffusion priors. The second direction focuses on Effects-Aware Editing Architectures that explicitly model intricate lighting, shadows, and reflections to anchor the edited object realistically within its environment, leveraging both spatial attention mechanisms and sequence-to-sequence temporal priors. The third direction investigates Generative Amodal Completion to automate the hallucination of occluded geometric structures, thereby eliminating the reliance on manual user intervention and enabling a fully automated layered editing pipeline. Finally, the fourth direction introduces Cycle-Consistency Optimization as an inference-time objective and fine-tuning strategy to ensure invertible, high-fidelity feature preservation, effectively solving the inversion degradation bottleneck. By synthesizing these advanced technical vectors, this report provides the foundational blueprint for a decoupled, structurally coherent, and physically grounded geometric image editing pipeline.

## Diagnostic Foundation: The Intrinsic Limits of Current Architectures

To propose viable architectural advancements, it is strictly necessary to diagnose the exact failure modes and performance ceilings of the current state-of-the-art. The baseline architecture analyzed herein operates on a training-free decoupled pipeline, which represents the current optimal approach for managing large structural edits without requiring dataset-specific fine-tuning.1

The decoupled pipeline operates in three sequential phases. Initially, a geometric transformation algorithm relocates the source object within the spatial bounds of the image, generating a coarse composite image and a corresponding target mask.1 For two-dimensional edits, this is an affine transformation matrix encompassing scaling, rotation, and translation parameters. For three-dimensional edits, the system utilizes monocular depth estimation to construct a sparse 3D point cloud, applies a rotation matrix in 3D space, and reprojects the coordinates back to the 2D plane.1 Following the transformation, the source region is inpainted to restore the exposed background.1 The final phase involves target region refinement, driven by a diffusion-based architecture that employs three complementary modules: Temporal Contextual Attention, Local Perturbation, and Content-specified Generation.1

Temporal Contextual Attention dynamically blends Mask-guided Mutual Self-Attention with full global self-attention across the denoising timesteps.1 This ensures that major structural changes occur in the early diffusion steps while relying on full self-attention in the later steps to harmonize local details.1 Local Perturbation introduces controlled stochasticity by selectively applying Denoising Diffusion Probabilistic Model updates exclusively within the user-defined edit masks, while retaining deterministic Denoising Diffusion Implicit Model updates elsewhere.1 Content-specified Generation utilizes localized textual cross-attention and classifier-free guidance to steer the synthesis of newly exposed regions based on semantic prompts.1

### Exhaustive Metric Reproduction and Stratification

To objectively localize the structural weaknesses of this architecture, a massive metric-driven diagnosis was executed across an extensive dataset containing thousands of diverse geometric editing instructions.1 The evaluation utilized an array of highly specialized generative metrics to assess fidelity, consistency, and precision.1 The core metrics include Subject Consistency, which measures the cosine similarity between the foreground DINOv2 features of the source and generated images; Background Consistency, which measures the CLIP feature similarity of the unedited regions; Warp Error, which computes the pixel-wise L1 error between a mathematically warped source object and the generated output; and Mean Distance, a stochastic metric utilizing Deep Image Feature Transfer keypoints to track semantic correspondence accuracy.1

The initial phase of the diagnostic study involved a full-scale reproduction of the baseline pipeline across all available single-type edits to establish the absolute performance baseline.1 The reproduction was executed under strictly controlled generation environments to ensure numerical neutrality.

The reproduction data confirms the stability of the baseline architecture, with all seven generative metrics falling within an acceptable margin of variance.1 The edit-precision metrics, Warp Error and Mean Distance, demonstrated marginal improvements due to refined noise floor seeding.1 Having established a verified baseline, the dataset was subsequently stratified by edit difficulty—normalized across translation magnitude, rotation angle, scale factor, and mask area—to isolate specific failure modes.1

The stratification data reveals a critical diagnostic signal. As the difficulty of the geometric instruction scales from easy to hard, the Subject Consistency metric collapses significantly from 0.942 to 0.865.1 Simultaneously, the Mean Distance metric nearly triples from 4.85 to 13.37, indicating severe structural degradation and loss of semantic keypoint correspondence.1 Crucially, the Background Consistency and Warp Error remain relatively flat across all difficulty tiers.1 This proves that the Local Perturbation masking strategy successfully isolates the background from unintended edits, and the model maintains high pixel-level fidelity within the target mask. The failure is entirely concentrated on the structural identity of the object under extreme transformations.

Further stratification by edit type isolates the exact nature of this structural collapse.1

The move operation (pure translation) represents a solved domain for this architecture, yielding an exceptional Subject Consistency of 0.959 and a minimal Mean Distance of 3.75.1 However, rotational and resizing operations drive the average Mean Distance up by a factor of three. In the hardest subgroups, rotational Mean Distance spikes to approximately 15.7, and resize Mean Distance reaches 16.5, with Subject Consistency dropping to the 0.83-0.85 range.1 The diagnostic conclusion is unequivocal: the architecture perfectly preserves background and refines pixels, but fundamentally loses the object's structural identity under large shape-changing edits.1

### Systematic Falsification of Algorithmic Deficiencies

To ascertain whether this structural failure on hard rotations and scaling is an addressable algorithmic deficiency or an intrinsic limitation of the diffusion prior, a rigorous, five-phase falsification sweep was executed against the baseline architecture.1 Each phase tested a specific hypothesis regarding the root cause of the structural collapse.

The first phase tested configuration and controllability.1 The hypothesis posited that the Temporal Contextual Attention injection start-step or the classifier-free guidance scales were sub-optimally tuned. Sweeping the start-step across a wide matrix (steps 25, 30, 40, and 45) and the modulated attention layers (layers 4, 8, 12) revealed that the Subject Consistency score remained rigidly pinned between 0.8517 and 0.8529 for hard rotations, and 0.8319 and 0.8414 for hard resizing.1 While aggressive classifier-free guidance yielded a narrow signal in the resize Mean Distance, the Subject Consistency remained unaffected. This confirms that the bottleneck is mechanistic, not an artifact of poor hyperparameter scheduling.1

The second phase evaluated input quality and structure-injection strength.1 The baseline utilizes a coarse warp as the input for refinement. The hypothesis suggested that aliasing in the coarse warp was destroying high-frequency structural details. The implementation of an anti-aliased supersampled-Lanczos warp resulted in a negligible Subject Consistency shift (0.8523 to 0.8537).1 Furthermore, artificially elevating the injection floor via an adaptive end-scale monotonically degraded the Mean Distance, proving that the baseline's decay schedule is already optimal.1

The third phase tested semantic-identity conditioning.1 If the model was simply "forgetting" the object identity during complex rotations, injecting semantic priors should resolve the issue. An IP-Adapter was integrated, feeding a cropped image prompt of the source object into the target mask.1 Sweeping the adapter scale from 0.5 to 1.4 resulted in a pristine, monotone degradation of rotational Subject Consistency, falling from 0.8523 down to 0.8502.1 The identity conditioning acts on a coarse, semantic token level ("what the object is"), whereas the failure mode is strictly geometric. Forcing semantic identity actively interferes with the geometric structural coherence required by the evaluation metrics.1

The fourth phase tackled the attention mechanism directly.1 The baseline Temporal Contextual Attention allows the target-pose query to attend to the original source-pose key and value through a column mask.1 However, there is no explicit geometric correspondence; matching relies entirely on feature similarity, which breaks down during severe affine transformations.1 Three geometry-aware attention mechanisms were implemented: a correspondence bias prioritizing spatially aligned tokens, warped key/value resampling to physically relocate source features to the target geometry, and a warped reference input.1 Every single variant lowered the Subject Consistency score.1 Most tellingly, these geometry-aligned mechanisms severely damaged the pure translation subgroup, dropping its Subject Consistency from 0.959 to as low as 0.937.1 The explicit enforcement of geometric correspondence introduced bilinear feature blur and over-sharpened attention artifacts, proving that the structural collapse lives downstream in the diffusion refinement itself, not in the attention correspondence.1

### The Perfect-Warp Ceiling

The final, decisive phase of the diagnostic study anchored the edit-branch latent heavily to the coarse, mathematically perfect in-plane warp during the denoising process.1 The blend strength was swept from 0.3 to 0.9, effectively pinning the diffusion generation to the optimal geometric transform.1

The dose response of the Subject Consistency metric is entirely flat across the preservation sweeps.1 Even when the object is mathematically pinned to the perfect in-plane warp (w=0.9), the Subject Consistency only rises a fraction of a percent over the baseline, plateauing at 0.8535.1

This provides a definitive architectural conclusion: the baseline refinement process already achieves approximately 99.9% of the perfect-warp ceiling.1 The apparent weakness on hard rotations and resizing is not an addressable algorithmic deficiency within the 2D diffusion module. It is a fundamental consequence of the in-plane transform itself and the extreme view-sensitivity of the feature extractors.1 Projecting a 3D object onto a 2D plane and rotating it purely in 2D mathematically distorts depth, perspective, and lighting cues, resulting in an output that physical feature extractors penalize heavily. Therefore, further iteration on 2D in-plane self-attention mechanisms is a functionally exhausted research vector. To achieve significant advancements in geometric editing, the architecture must transition to out-of-plane novel-view synthesis, explicitly model environmental lighting effects, incorporate amodal occlusion reasoning, and enforce strict cycle-consistency objectives.

## Advancing Out-of-Plane Manipulation via Novel-View Synthesis

The reliance on monocular depth estimation represents the most significant structural bottleneck for current geometric editing pipelines when attempting three-dimensional transformations.1

The standard approach to 3D editing involves estimating the scene depth using a relative depth estimator to establish a sparse 3D representation.1 The segmented object is lifted into 3D space using an assumed camera intrinsic matrix, transformed via a specific rotation matrix, and reprojected back to the 2D image plane.1 This paradigm suffers from critical failure modes. First, the camera intrinsic matrix is rarely known for single-image edits and must be heuristically estimated, leading to severe perspective distortion. Second, relative depth maps lack metric accuracy, causing geometric flattening. Third, and most importantly, rotating a sparse 2D point cloud exposes unseen back-faces of the object, resulting in massive data voids (holes) during reprojection.1 The subsequent diffusion refinement module is forced to hallucinate these missing textures without any 3D prior, leading to structurally implausible generations and the low Subject Consistency scores identified in the diagnostic sweep.1

Attempts to bypass this by leveraging early multi-view video diffusion models face different challenges.1 While models like SV3D can generate a sequence of frames representing different azimuth and elevation angles, they require the source object to be segmented and placed on a clean white background prior to generation.1 Consequently, the transformed objects suffer from severe high-frequency detail loss and structural artifacts during extraction and recompositing.1 The generated object often loses its textural relationship with the original image, appearing as a smoothed, artificial asset.

### Pixel-Splatting and Latent Video Priors

To overcome these limitations, the geometric transformation module must be entirely replaced by an integrated Single-Image Novel-View Synthesis (NVS) architecture. The proposed architectural shift transitions away from discrete depth-lifting and embraces pixel-space diffusion models explicitly trained for end-to-end novel view generation.3

Recent advancements in NVS demonstrate that encoding geometric information directly into the diffusion network yields minor improvements compared to utilizing scaled, high-capacity generative models trained on massive single-view and multi-view datasets.3 However, to maintain the strict structural fidelity required for geometric editing, the architecture will integrate a pixel-splatting-guided video diffusion model.5

Unlike standard latent video diffusion models that generate views independently in the latent space, pixel-splatting-guided models enforce explicit geometric consistency.5 The source object is processed through a pixel-splatting mechanism that forward-warps the visible pixels to the target view based on a continuously refined internal depth map.5 This splatted representation acts as a highly accurate spatial conditioning signal for the diffusion backbone. By injecting this splatted feature map into the cross-attention layers of the U-Net, the model achieves an aligned synthesis that precisely controls the novel view while maintaining the exact high-fidelity texture of the original source image.5 This approach seamlessly bridges the gap between single-view NVS and stereo video conversion, ensuring that the generated object retains its micro-textures and complex boundaries without the smoothing artifacts associated with white-background multi-view generation.

In practice, the user's geometric edit instruction is parsed into specific azimuth, elevation, and scaling deltas.1 The pixel-splatting NVS module synthesizes the target view, generating both the transformed object and a highly precise target mask.5 The composite image is then constructed by blending the NVS output with the inpainted background. Because the NVS module natively handles the hallucination of previously occluded textures using a robust 3D prior, the burden on the downstream Temporal Contextual Attention refinement module is drastically reduced. The refinement phase is relegated to its optimal function: harmonizing the boundary lighting and blending the object seamlessly into the background, rather than structurally reconstructing unseen geometries.

## Effects-Aware Editing Architectures and Physical Grounding

Even with perfect out-of-plane novel-view synthesis, a geometrically transformed object will inherently look artificial—appearing to float or sit unnaturally within the scene—if the environmental lighting effects are ignored.6 The metric-driven diagnosis highlights effects-awareness as a glaring, largely unaddressed realism gap in current decoupled pipelines.1 When an object is moved, rotated, or scaled, its shadow trajectory, ambient occlusion, and surface reflections must dynamically update to reflect the new spatial coordinates relative to the scene's light sources.6

Standard diffusion models fail to achieve this because their self-attention mechanisms statistically bias attention distribution based on texture and semantic similarity, rather than modeling physical light transport.8 Two distinct architectural paradigms are proposed to resolve this: static spatial attention manipulation and temporal sequence-to-sequence video priors.

### Spatial Attention Manipulation: Effects-Sensitive Attention

The first architectural approach modifies the spatial cross-attention layers of the refinement U-Net to explicitly calculate environmental lighting, drawing inspiration from frameworks such as GeoEdit.9

In a standard decoupled pipeline, the refinement mask is strictly defined by the target object mask.1 For effects-aware editing, the architecture must automatically calculate an expanded "Effects Radius" mask that encompasses the surfaces adjacent to and beneath the target object, where shadows and reflections are physically expected to occur.6

The standard self-attention module is augmented with Effects-Sensitive Attention.11 Within the designated effects mask, the query vectors are explicitly directed to cross-attend to the latent features of the background scene, specifically regions identified as primary illumination sources.10 This biased attention routing forces the network to condition the synthesis of the effects region on the global lighting context, generating shadows with appropriate opacity, edge softness, and directional trajectories.

To train this highly specialized attention mechanism, the architecture requires datasets that contain paired images of identical scenes with varying geometric object placements and ground-truth shadow mapping. The proposed pipeline will leverage large-scale geometric editing datasets such as RS-Objects.8 Constructed via a two-stage rendering-to-synthesis pipeline utilizing modern game engines and Blender, RS-Objects contains over 120,000 high-quality image-mask pairs covering diverse object categories and complex scenes, providing the precise geometric and texture cues necessary to train the Effects-Sensitive Attention module.8

Furthermore, while shadow generation has seen some exploration, surface reflection generation remains critically underexplored.6 To address this, the architecture will integrate a dedicated ControlNet encoder fine-tuned on the DEROBA dataset, the first large-scale object reflection dataset.6 The ControlNet encoder accepts the composite image and the composite foreground mask, injecting strong prior information regarding reflection placement and appearance into the diffusion model, enabling the generation of physically coherent reflections on specular surfaces.6

### Temporal Approaches: Sequence-to-Sequence Video Priors

An alternative, potentially more robust architectural paradigm models geometric editing not as a spatial inpainting task, but as a temporal sequence-to-sequence problem.7 Borrowing from the ObjectMover architecture, the pipeline fine-tunes a video generation foundation model to leverage its inherent knowledge of consistent object generation and lighting synchronization across frames.7

In this framework, the original source image serves as Frame 0, and the edited target image is formulated as Frame N. The motion trajectory from the source mask to the target mask dictates the temporal flow. Video diffusion priors inherently understand that as an object translates across a surface, its shadow must continuously adapt to the changing geometry of the ground plane.7 By utilizing a multi-task learning strategy that combines high-quality synthetic data pairs generated from modern game engines with real-world video data, the model gains a versatile capability to handle extreme lighting harmonization, perspective adjustments, and complex occlusion relationships.7

For multi-round editing—where a user performs sequential transformations over a sustained session—the pipeline can adopt a 3D-aware autoregressive framework similar to the Free-Form Scene Editor (FFSE).2 FFSE models editing as a sequence of learned 3D transformations, utilizing a hybrid loss function that combines reconstruction quality, geometric consistency constraints, and environmental effect preservation.13 Trained on datasets like 3DObjectEditor, which consists of simulated editing sequences across dynamic scenes, this autoregressive approach ensures that shadows and reflections remain globally consistent and physically plausible across an arbitrary number of iterative edits, preventing the scene degradation common in single-turn editing frameworks.2

## Generative Amodal Completion for Occlusion Handling

A fundamental limitation of current geometric editing pipelines arises when dealing with occluded objects. In the baseline architecture, if an object is moved from behind an occluding barrier (e.g., moving a vehicle partially hidden by a tree), the newly exposed regions of the object must be synthesized. The baseline addresses this by requiring the user to manually draw a structure completion mask and provide a content-specified text prompt.1 This manual intervention disrupts the automation of the pipeline, introduces human error, and limits the framework's viability for high-throughput or programmatic editing tasks.

To construct a fully automated, layered editing pipeline, the architecture must natively possess a concept of object permanence. The proposed solution involves entirely replacing manual user masks with Generative Amodal Completion modules. Amodal segmentation and completion aim to infer the complete geometric shape and textural appearance of an object, even when substantial portions of it are occluded by foreground elements.14

### Promptable Amodal Inference and LLM Reasoning

The first phase of the amodal pipeline involves predicting the true geometric boundary of the occluded object. Before the source object is extracted and transformed, the system performs an amodal reasoning pass. The architecture will utilize advanced reasoning segmentors, inspired by frameworks like AURA (Amodal Understanding and Reasoning Assistant), which integrate multi-modal Large Language Models to reason about complex, real-world occlusions based on contextual scene understanding.14

To provide fine-grained control over the hallucinated geometry, the pipeline will incorporate promptable human amodal completion (PHAC) networks.15 PHAC addresses the issue of unconstrained hallucination by allowing the injection of simple point-based prompts—such as estimated joint locations for a partially hidden human figure, or bounding boxes defining the expected spatial extent of an object.15 These prompts are encoded using specialized ControlNet modules and injected into the pre-trained diffusion model's cross-attention blocks, ensuring strict prompt alignment without degrading the underlying generative prior.15

### Video Diffusion Priors for Temporal Amodal Segmentation

In scenarios involving extreme occlusion where single-frame reasoning is highly ambiguous, the pipeline will deploy video diffusion priors for amodal segmentation.16 Video foundation models inherently possess object permanence cues learned from tracking objects through full occlusion events across time.

By repurposing a latent video diffusion model, the architecture can condition the generation on a sequence of modal (visible) mask frames alongside contextual depth maps.16 The memory-efficient interleaving of spatial and temporal layers within the diffusion transformer allows the network to logically hallucinate the complete boundary of the object based on its trajectory and surrounding depth cues.16 This approach has demonstrated dramatic improvements in segmenting highly occluded regions compared to pure image-based methods.16

### Decomposed Inpainting and Layered Compositing

Once the amodal boundary is accurately predicted, the occluded regions must be filled with coherent, high-fidelity textures prior to applying any geometric transformations.16 If a transformation matrix or novel-view synthesis is applied to a hollow or partially complete object, the resulting output will suffer from severe distortion.

The content completion phase utilizes a specialized inpainting-based refinement module.15 This module starts with a slightly noised coarse completion within the hallucinated amodal boundary. By heavily preserving the latent features of the visible regions, the diffusion process ensures seamless textural blending and structural continuity across the occlusion boundary.15

Upon completion of the inpainting phase, the fully realized, unoccluded object is packaged as an independent digital asset within a localized latent space. This layered editing approach allows the object to be freely translated, rotated, or scaled in its canonical frame without carrying over any occluding artifacts or jagged boundaries from the source scene, representing a massive leap in geometric editing precision.1

## Cycle-Consistency and Equivariance Objectives

The final critical vector for architectural improvement addresses the fundamental algorithmic mechanics of the diffusion refinement process. The vast majority of diffusion-based editing techniques, including the baseline pipeline, rely heavily on an initial inversion step—mapping the source image back to a latent noise representation using techniques such as Denoising Diffusion Implicit Model (DDIM) inversion.1

Inversion processes are inherently lossy. When scaling these pipelines for rapid inference using distilled diffusion models or latent consistency models, the inversion quality degrades rapidly. Poor inversion fails to preserve the high-frequency structural details and semantic integrity of the source image.17 Consequently, any subsequent edits applied during the forward generation phase suffer from global artifacting, color shifts, and identity drift, phenomena explicitly observed in the failure cases of the baseline architecture.1 Furthermore, as diagnosed in the metric evaluations, standard spatial attention mechanisms struggle to maintain structural fidelity without strict geometric correspondence guarantees.1

### Invertible Consistency Distillation and Perceptual Loss

To resolve the inversion bottleneck and enforce strict structural preservation during geometric edits, the architecture must integrate Cycle-Consistency Optimization. The principle of equivariance and cycle consistency dictates a fundamental mathematical constraint: applying a geometric edit followed by the exact inverse edit should yield the identity function, perfectly reconstructing the original image without degradation.1

The proposed pipeline will integrate an Invertible Consistency framework inspired by Inverse-and-Edit.17 This architecture abandons standard DDIM inversion and iterative optimization in favor of a dual consistency model paradigm.22 The system employs a forward consistency model () explicitly trained to map an image back to its prior latent space in a minimal number of steps (typically four), alongside a corresponding backward generation model ().21

The critical innovation in this framework is the application of a perceptual reconstruction loss across the entire forward-backward cycle, rather than optimizing segment-wise in the latent space.22 The cycle-consistency loss is defined mathematically as:

In this formulation,  represents the source target region.22 The function  denotes the multi-step forward inversion process utilizing the forward consistency model and the Variational Autoencoder (VAE) encoder.22 Conversely,  represents the multi-step backward generation process using the backward consistency model and the VAE decoder.22 The Learned Perceptual Image Patch Similarity (LPIPS) metric, utilizing a VGG-16 backbone, calculates the perceptual divergence between the original image and the full-cycle reconstruction.22

By fine-tuning the consistency models using complete end-to-end backpropagation across the entire VAE boundary, the architecture achieves a highly controllable trade-off between editability—adhering strictly to the target geometric transform—and absolute content preservation.17 This entirely eliminates the need for computationally heavy feature-injection mechanisms like Prompt-to-Prompt, streamlining the editing process while vastly improving structural fidelity.17

### Inversion-Free Flow-Based Optimization

In highly constrained computational environments where full-cycle gradient backpropagation through the VAE is prohibitive, the architecture can seamlessly pivot to an inversion-free, flow-based editing framework, conceptually aligned with FlowCycle.23

In this architectural variant, the geometric transformation corruption is mathematically parameterized using learnable noise vectors rather than explicit latent inversion.23 The optimization process enforces dual consistency constraints: iteratively editing the source to the target state, while simultaneously calculating the recovery flow back to the source.23 This bidirectional optimization allows the network to learn a target-aware intermediate latent state that inherently respects the original geometric structure, enabling faithful modifications while preserving absolute source consistency, all while dynamically adjusting sampling steps for inference efficiency.23

### Inference-Time Guidance and Validation

Beyond serving as a robust fine-tuning strategy, cycle-consistency can be deployed as an active inference-time guidance objective.1 During the denoising steps of the target region refinement phase, the gradients derived from the cycle-consistency loss can be utilized to dynamically steer the latent trajectory. If a complex rotation or severe scaling operation begins to warp the structural identity of the object—detected as a rapidly diverging  during a simulated inverse-transform check—the inference-time guidance dynamically corrects the latent code. This real-time validation acts as a mathematical safeguard, effectively preventing the catastrophic structural collapse observed in the hard-edit evaluation subgroups and pushing the architecture beyond the current perfect-warp ceiling.

## Synthesis and Conclusion

The exhaustive metric-driven evaluation of existing training-free geometric image editors unequivocally confirms that while in-plane spatial manipulations are highly optimized, deep structural edits requiring three-dimensional comprehension face a strict mathematical ceiling. The degradation of subject-structural fidelity during complex rotations is not a symptom of suboptimal hyperparameter tuning or insufficient attention guidance. It is a fundamental consequence of attempting to solve out-of-plane geometric tasks using purely two-dimensional self-attention mechanisms and lossy monocular depth reprojection.1

To achieve the next paradigm of geometric image editing, architectures must evolve beyond decoupled boundary blending and embrace a structurally coherent, physically grounded blueprint.

The proposed next-generation pipeline orchestrates these advanced technical vectors into a unified workflow. The process initiates with Amodal Scene Parsing, where foundation amodal segmentors and video diffusion priors hallucinate invisible boundaries and inpaint occluded textures, rendering the target object as a fully realized, independent digital asset.14 Concurrently, cycle-consistent background inpainting modules restore the source region.1

The fully unoccluded asset is then passed into a Single-Image Novel-View Synthesis module. Utilizing pixel-splatting-guided diffusion, the object is lifted, rotated out-of-plane, and resynthesized with perfect geometric and textural fidelity, bypassing the severe artifacting associated with standard depth-lifting or white-background multi-view generation.5

Following the geometric transformation, the object is composited into the target location. The diffusion refinement U-Net, augmented with Effects-Sensitive Attention and fine-tuned on specialized rendering-to-synthesis datasets, explicitly calculates environmental lighting.8 By querying global illumination features, the pipeline casts accurate shadows and synthesizes physical surface reflections, ensuring the object interacts dynamically with its environment.6

Finally, the entire generation cycle is governed by strict Cycle-Consistency Optimization. Utilizing fast forward-backward consistency models and full-cycle perceptual reconstruction losses, the architecture ensures that the high-frequency textural details and semantic identity of the original amodal asset are perfectly preserved during the final blending steps.21

The execution of these proposed architectural experiments will successfully transition geometric image editing from a superficial 2D pixel-manipulation task into an intelligent, physically grounded, 3D-aware simulation framework capable of seamless, multi-round scene modification.

Πηγές αναφοράς

FreeFine.pdf

Free-Form Scene Editor: Enabling Multi-Round Object Manipulation like in a 3D Engine, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2511.13713v1

CVPR Poster Novel View Synthesis with Pixel-Space Diffusion Models, πρόσβαση Ιουνίου 25, 2026, https://cvpr.thecvf.com/virtual/2025/poster/33385

Novel View Synthesis with Pixel-Space Diffusion Models - CVF Open Access, πρόσβαση Ιουνίου 25, 2026, https://openaccess.thecvf.com/content/CVPR2025/papers/Elata_Novel_View_Synthesis_with_Pixel-Space_Diffusion_Models_CVPR_2025_paper.pdf

High-Fidelity Novel View Synthesis via Splatting-Guided Diffusion - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2502.12752v1

Reflection Generation for Composite Image Using Diffusion Model - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2604.02168v1

CVPR Poster ObjectMover: Generative Object Movement with Video Prior, πρόσβαση Ιουνίου 25, 2026, https://cvpr.thecvf.com/virtual/2025/poster/33409

Geometric Image Editing via Effects-Sensitive In-Context Inpainting with Diffusion Transformers | OpenReview, πρόσβαση Ιουνίου 25, 2026, https://openreview.net/forum?id=0JfUjV1uIS

[2602.08388] Geometric Image Editing via Effects-Sensitive In-Context Inpainting with Diffusion Transformers - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/abs/2602.08388

Geometric Image Editing via Effects-Sensitive In-Context Inpainting with Diffusion Transformers - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2602.08388

Geometric Image Editing via Effects-Sensitive In-Context Inpainting with Diffusion Transformers | Request PDF - ResearchGate, πρόσβαση Ιουνίου 25, 2026, https://www.researchgate.net/publication/400603806_Geometric_Image_Editing_via_Effects-Sensitive_In-Context_Inpainting_with_Diffusion_Transformers

ObjectMover: Generative Object Movement with Video Prior - IEEE Computer Society, πρόσβαση Ιουνίου 25, 2026, https://www.computer.org/csdl/proceedings-article/cvpr/2025/436400r682/299cgKWtI9G

Free-Form Scene Editor: Enabling Multi-Round Object Manipulation Like in a 3D Engine - Henghui Ding, πρόσβαση Ιουνίου 25, 2026, https://henghuiding.com/FFSE/

Reasoning Complex Occlusions Amodally with AURA - ICCV 2025 Open Access Repository, πρόσβαση Ιουνίου 25, 2026, https://openaccess.thecvf.com/content/ICCV2025/html/Li_Unveiling_the_Invisible_Reasoning_Complex_Occlusions_Amodally_with_AURA_ICCV_2025_paper.html

PHAC: Promptable Human Amodal Completion - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2603.14741v1

CVPR Poster Using Diffusion Priors for Video Amodal Segmentation, πρόσβαση Ιουνίου 25, 2026, https://cvpr.thecvf.com/virtual/2025/poster/34272

Inverse-and-Edit: Effective and Fast Image Editing by Cycle Consistency Models - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2506.19103v1

Inverse-and-Edit: Effective and Fast Image Editing by Cycle Consistency Models - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/abs/2506.19103

Inverse-and-Edit: Effective and Fast Image Editing by Cycle Consistency Models - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/pdf/2506.19103

ControlGenAI/Inverse-and-Edit - GitHub, πρόσβαση Ιουνίου 25, 2026, https://github.com/ControlGenAI/Inverse-and-Edit/

Inverse-and-Edit: Simple and Effective Framework for Fast Image Editing | OpenReview, πρόσβαση Ιουνίου 25, 2026, https://openreview.net/forum?id=1THHanty0x

[Literature Review] Inverse-and-Edit: Effective and Fast Image Editing by Cycle Consistency Models - Moonlight, πρόσβαση Ιουνίου 25, 2026, https://www.themoonlight.io/en/review/inverse-and-edit-effective-and-fast-image-editing-by-cycle-consistency-models

[2510.20212] Target-aware Image Editing via Cycle-consistent Constraints - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/abs/2510.20212

(PDF) FlowCycle: Pursuing Cycle-Consistent Flows for Text-based, πρόσβαση Ιουνίου 25, 2026, https://www.researchgate.net/publication/396847889_FlowCycle_Pursuing_Cycle-Consistent_Flows_for_Text-based_Editing

FlowCycle: Pursuing Cycle-Consistent Flows for Text-based Editing - arXiv, πρόσβαση Ιουνίου 25, 2026, https://arxiv.org/html/2510.20212v1


### Table 1


| Metric | Original Reported Value | Reproduced Value | Variance |

| --- | --- | --- | --- |

| Fréchet Inception Distance (FID) ↓ | 34.72 | 35.04 | +0.9% |

| DINOv2 Feature Distance ↓ | 478.18 | 487.82 | +2.0% |

| Kernel Distance (KD) ↓ | 0.144 | 0.142 | −1.2% |

| Subject Consistency (SUBC) ↑ | 0.907 | 0.911 | +0.4% |

| Background Consistency (BGC) ↑ | 0.971 | 0.967 | −0.4% |

| Warp Error (WE) ↓ | 0.055 | 0.047 | −14.5% |

| Mean Distance (MD) ↓ | 9.25 | 8.50 | −8.1% |


### Table 2


| Difficulty Stratification | Subject Consistency ↑ | Background Consistency ↑ | Warp Error ↓ | Mean Distance ↓ |

| --- | --- | --- | --- | --- |

| Easy | 0.942 | 0.971 | 0.046 | 4.85 |

| Medium | 0.927 | 0.966 | 0.046 | 6.98 |

| Hard | 0.865 | 0.964 | 0.050 | 13.37 |


### Table 3


| Edit Type Stratification | Subject Consistency ↑ | Background Consistency ↑ | Warp Error ↓ | Mean Distance ↓ |

| --- | --- | --- | --- | --- |

| Move (Translation) | 0.959 | 0.967 | 0.049 | 3.75 |

| Rotate | 0.901 | 0.967 | 0.043 | 10.43 |

| Resize | 0.892 | 0.967 | 0.049 | 9.96 |


### Table 4


| Refinement Preservation Blend Strength | Rotate Hard SUBC ↑ | Resize Hard SUBC ↑ | All 200 SUBC ↑ | Warp Error ↓ |

| --- | --- | --- | --- | --- |

| Baseline (w = 0) | 0.8523 | 0.8391 | 0.9154 | 0.0488 |

| Blend w = 0.3 | 0.8536 | 0.8409 | 0.9175 | 0.0454 |

| Blend w = 0.5 | 0.8535 | 0.8404 | 0.9174 | 0.0453 |

| Blend w = 0.7 | 0.8535 | 0.8400 | 0.9174 | 0.0453 |

| Blend w = 0.9 | 0.8535 | 0.8399 | 0.9174 | 0.0453 |