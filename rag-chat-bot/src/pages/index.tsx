import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';
import Heading from '@theme/Heading';
import CuteClock from '@site/src/components/CuteClock';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <CuteClock />
      <div className={clsx("container", styles.heroContainer)}>
        <div className={styles.heroImage}>
            <img src="img/ai-robot.png" alt="AI Robot" className={styles.robotImage} />
        </div>
        <div className={styles.heroContent}>
            <Heading as="h1" className="hero__title">
            {siteConfig.title}
            </Heading>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
            <div className={styles.buttons}>
            <Link
                className="button button--secondary button--lg"
                to="/docs/intro">
                AI BOOK CREATED BY ZAHID IMAM
            </Link>
            </div>
        </div>
      </div>
    </header>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
