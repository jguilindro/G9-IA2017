import tensorflow as tf
import numpy as np
tf.logging.set_verbosity(tf.logging.INFO)

def ANN_train(training_input, training_target,epochs=1):
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[20])]

    # Build a DNN
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[30],
                                            n_classes=5,
                                            model_dir="./tmp/course_difficulty_model",
                                            config=tf.contrib.learn.RunConfig(save_checkpoints_steps=10))

    # Define the training inputs
    train_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(training_input)},
                                                        y=np.array(training_target),
                                                        num_epochs=epochs,
                                                        shuffle=True)

    # Train model.
    classifier.train(input_fn=train_input_fn)

def ANN_predict(new_samples):
    # Specify that all features have real-value data
    feature_columns = [tf.feature_column.numeric_column("x", shape=[20])]

    # Build a DNN
    classifier = tf.estimator.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[30],
                                            n_classes=5,
                                            model_dir="./tmp/course_difficulty_model",
                                            config=tf.contrib.learn.RunConfig(save_checkpoints_steps=1))

    predict_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": np.array(new_samples)},
                                                        num_epochs=1,
                                                        shuffle=False)

    predictions = list(classifier.predict(input_fn=predict_input_fn))
    predicted_classes = [p["classes"] for p in predictions]

    return predicted_classes


def main():
    training_input = [np.full((20),1),np.full((20),2),np.full((20),3)]
    training_target = [1,2,3]
    test_input = [np.full((20),1),np.full((20),2),np.full((20),3)]
    ANN_train(training_input,training_target,epochs=5)
    print 'Classifier response: {}'.format(ANN_predict(test_input))
